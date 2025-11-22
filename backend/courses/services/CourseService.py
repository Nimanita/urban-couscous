"""
courses/services.py - Course business logic
"""
from django.db import transaction
from django.db.models import Count, Sum, Q
from ..models import Course, Lesson
from report.models import Progress


class CourseService:
    """Service class for course operations"""
    
    @staticmethod
    def get_all_courses(is_published=True):
        """Get all courses"""
        try:
            courses = Course.objects.filter(is_published=is_published).select_related()
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
    def get_courses_with_student_progress(student):
        """Get all courses with student progress"""
        try:
            courses = Course.objects.filter(is_published=True).prefetch_related('lessons')
            
            course_data = []
            for course in courses:
                total_lessons = course.lessons.count()
                completed_lessons = Progress.objects.filter(
                    student=student,
                    lesson__course=course,
                    status='completed'
                ).count()
                
                progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
                
                # Calculate total time spent on this course
                time_spent = Progress.objects.filter(
                    student=student,
                    lesson__course=course
                ).aggregate(total=Sum('time_spent_minutes'))['total'] or 0
                
                course_data.append({
                    'course': course,
                    'total_lessons': total_lessons,
                    'completed_lessons': completed_lessons,
                    'progress_percentage': round(progress_percentage, 2),
                    'time_spent_minutes': time_spent,
                    'status': 'completed' if progress_percentage == 100 else ('in_progress' if progress_percentage > 0 else 'not_started')
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


