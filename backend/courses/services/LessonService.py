
from django.db import transaction
from ..models import Course, Lesson


class LessonService:
    """Service class for lesson operations"""
    
    @staticmethod
    def get_lessons_by_course(course_id, student=None):
        """Get all lessons for a course with optional student progress (OPTIMIZED)"""
        try:
            # Fetch all lessons with course data in one query
            lessons = Lesson.objects.filter(
                course_id=course_id
            ).select_related('course').order_by('order')
            
            if student:
                # Import ProgressService here to avoid circular import
                from report.services.ProgressService import ProgressService
                
                # Get all lesson IDs
                lesson_ids = [lesson.id for lesson in lessons]
                
                # Fetch ALL progress records in ONE service call
                # This replaces the N individual queries with just 1 query
                progress_result = ProgressService.get_progress_for_lessons(
                    student, 
                    lesson_ids
                )
                
                if not progress_result['success']:
                    return progress_result
                
                progress_dict = progress_result['progress_dict']
                
                # Build response data with O(1) lookups
                lesson_data = []
                for lesson in lessons:
                    # Default progress info if none exists
                    progress_info = progress_dict.get(lesson.id, {
                        'status': 'not_started',
                        'time_spent_minutes': 0,
                        'completed_at': None,
                        'last_accessed': None,
                        'notes': ''
                    })
                    
                    lesson_data.append({
                        'lesson': lesson,
                        'progress': progress_info
                    })
                
                return {'success': True, 'data': lesson_data}
            
            return {'success': True, 'lessons': lessons}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_lesson_by_id(lesson_id):
        """Get lesson by ID"""
        try:
            lesson = Lesson.objects.select_related('course').get(id=lesson_id)
            return {'success': True, 'lesson': lesson}
        except Lesson.DoesNotExist:
            return {'success': False, 'error': 'Lesson not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def create_lesson(course_id, title, description, content_type, order, estimated_minutes):
        """Create a new lesson"""
        try:
            with transaction.atomic():
                course = Course.objects.get(id=course_id)
                lesson = Lesson.objects.create(
                    course=course,
                    title=title,
                    description=description,
                    content_type=content_type,
                    order=order,
                    estimated_minutes=estimated_minutes
                )
                return {'success': True, 'lesson': lesson}
        except Course.DoesNotExist:
            return {'success': False, 'error': 'Course not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}