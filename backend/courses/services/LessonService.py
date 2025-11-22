"""
courses/services.py - Course business logic
"""
from django.db import transaction
from ..models import Course, Lesson
from report.models import Progress


class LessonService:
    """Service class for lesson operations"""
    
    @staticmethod
    def get_lessons_by_course(course_id, student=None):
        """Get all lessons for a course with optional student progress"""
        try:
            lessons = Lesson.objects.filter(course_id=course_id).order_by('order')
            
            if student:
                lesson_data = []
                for lesson in lessons:
                    try:
                        progress = Progress.objects.get(student=student, lesson=lesson)
                        progress_info = {
                            'status': progress.status,
                            'time_spent_minutes': progress.time_spent_minutes,
                            'completed_at': progress.completed_at,
                            'last_accessed': progress.last_accessed,
                            'notes': progress.notes
                        }
                    except Progress.DoesNotExist:
                        progress_info = {
                            'status': 'not_started',
                            'time_spent_minutes': 0,
                            'completed_at': None,
                            'last_accessed': None,
                            'notes': ''
                        }
                    
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