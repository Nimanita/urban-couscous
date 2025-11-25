
from django.db import transaction
from django.db.models import Sum, Count, Q
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
        """Get all published courses with their lesson counts (OPTIMIZED)"""
        try:
            courses = Course.objects.filter(
                is_published=True
            ).prefetch_related('lessons').annotate(
                lesson_count=Count('lessons')
            )
            
            course_data = []
            for course in courses:
                course_data.append({
                    'course': course,
                    'total_lessons': course.lesson_count
                })
            
            return {'success': True, 'data': course_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_courses_with_student_progress(student):
        """Get all courses with student progress (OPTIMIZED - SERVICE LAYER)"""
        try:
            from report.services.ProgressService import ProgressService
            
            # Get all courses with lessons
            courses = Course.objects.filter(
                is_published=True
            ).prefetch_related('lessons')
            
            # Collect all lesson IDs across all courses
            all_lesson_ids = []
            course_lesson_map = {}  # course_id -> [lesson_ids]
            
            for course in courses:
                lesson_ids = [lesson.id for lesson in course.lessons.all()]
                all_lesson_ids.extend(lesson_ids)
                course_lesson_map[course.id] = lesson_ids
            
            # Single batch call to ProgressService
            progress_result = ProgressService.get_progress_for_lessons(
                student,
                all_lesson_ids
            )
            
            if not progress_result['success']:
                return progress_result
            
            progress_dict = progress_result['progress_dict']
            
            # Calculate statistics for each course
            course_data = []
            for course in courses:
                lesson_ids = course_lesson_map[course.id]
                total_lessons = len(lesson_ids)
                
                completed_count = 0
                total_time = 0
                
                for lesson_id in lesson_ids:
                    if lesson_id in progress_dict:
                        prog = progress_dict[lesson_id]
                        if prog['status'] == 'completed':
                            completed_count += 1
                        total_time += prog['time_spent_minutes'] or 0
                
                progress_percentage = (
                    (completed_count / total_lessons * 100) 
                    if total_lessons > 0 else 0
                )
                
                course_data.append({
                    'course': course,
                    'total_lessons': total_lessons,
                    'completed_lessons': completed_count,
                    'progress_percentage': round(progress_percentage, 2),
                    'time_spent_minutes': total_time,
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