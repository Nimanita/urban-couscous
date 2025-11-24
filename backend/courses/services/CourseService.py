"""
courses/services/CourseService.py - Course business logic
"""
from django.db import transaction
from django.db.models import Sum
from ..models import Course, Lesson


class CourseService:
    """Service class for course operations"""
    
    @staticmethod
    def get_all_courses(is_published=True):
        """Get all courses"""
        try:
            courses = Course.objects.filter(is_published=is_published)
            return {'success': True, 'courses': courses}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_course_by_id(course_id):
        """Get course by ID"""
        try:
            course = Course.objects.get(id=course_id)
            return {'success': True, 'course': course}
        except Course.DoesNotExist:
            return {'success': False, 'error': 'Course not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_total_published_lessons_count():
        """Get total count of all published lessons across all courses"""
        try:
            count = Lesson.objects.filter(course__is_published=True).count()
            return {'success': True, 'count': count}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_courses_with_lesson_counts():
        """Get all published courses with their lesson counts"""
        try:
            courses = Course.objects.filter(
                is_published=True
            ).prefetch_related('lessons')
            
            course_data = []
            for course in courses:
                course_data.append({
                    'course': course,
                    'total_lessons': course.lessons.count()
                })
            
            return {'success': True, 'data': course_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_courses_with_student_progress(student):
        """Get all courses with student progress"""
        try:
            # Import ProgressService here to avoid circular import
            from report.services.ProgressService import ProgressService
            
            courses = Course.objects.filter(is_published=True).prefetch_related('lessons')
            
            course_data = []
            for course in courses:
                total_lessons = course.lessons.count()
                
                # Get completed lessons from ProgressService
                completed_result = ProgressService.get_completed_lessons_for_course(
                    student, 
                    course.id
                )
                if not completed_result['success']:
                    continue
                
                completed_lessons = completed_result['count']
                progress_percentage = (
                    (completed_lessons / total_lessons * 100) 
                    if total_lessons > 0 else 0
                )
                
                # Get time spent from ProgressService
                time_result = ProgressService.get_time_spent_for_course(student, course.id)
                time_spent = time_result['time_spent'] if time_result['success'] else 0
                
                course_data.append({
                    'course': course,
                    'total_lessons': total_lessons,
                    'completed_lessons': completed_lessons,
                    'progress_percentage': round(progress_percentage, 2),
                    'time_spent_minutes': time_spent,
                    'status': (
                        'completed' if progress_percentage == 100 
                        else ('in_progress' if progress_percentage > 0 else 'not_started')
                    )
                })
            
            return {'success': True, 'data': course_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def create_course(title, description, category, difficulty, estimated_hours):
        """Create a new course"""
        try:
            with transaction.atomic():
                course = Course.objects.create(
                    title=title,
                    description=description,
                    category=category,
                    difficulty=difficulty,
                    estimated_hours=estimated_hours
                )
                return {'success': True, 'course': course}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_lesson_count_for_course(course_id):
        """Get total lessons for a specific course"""
        try:
            count = Lesson.objects.filter(course_id=course_id).count()
            return {'success': True, 'count': count}
        except Exception as e:
            return {'success': False, 'error': str(e)}