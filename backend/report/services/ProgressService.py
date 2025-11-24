"""
report/services/ProgressService.py - Progress tracking business logic
"""
from django.db import transaction
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from ..models import Progress, Activity


class ProgressService:
    """Service class for progress operations"""
    
    @staticmethod
    def get_or_create_progress(student, lesson):
        """Get or create progress record"""
        try:
            progress, created = Progress.objects.get_or_create(
                student=student,
                lesson=lesson,
                defaults={'status': 'not_started'}
            )
            return {'success': True, 'progress': progress, 'created': created}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def update_progress(student, lesson_id, status=None, time_spent=None, notes=None):
        """Update progress for a lesson"""
        try:
            with transaction.atomic():
                progress, created = Progress.objects.get_or_create(
                    student=student,
                    lesson_id=lesson_id,
                    defaults={'status': 'in_progress'}
                )
                
                if status:
                    progress.status = status
                    if status == 'completed' and not progress.completed_at:
                        progress.completed_at = timezone.now()
                        # Create activity record
                        Activity.objects.create(
                            student=student,
                            lesson=progress.lesson,
                            event_type='lesson_complete',
                            duration_minutes=time_spent or 0,
                            date=timezone.now().date()
                        )
                
                if time_spent is not None:
                    progress.time_spent_minutes += time_spent
                
                if notes is not None:
                    progress.notes = notes
                
                progress.last_accessed = timezone.now()
                progress.save()
                
                return {'success': True, 'progress': progress}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def mark_lesson_complete(student, lesson_id, time_spent=0):
        """Mark a lesson as complete"""
        return ProgressService.update_progress(
            student=student,
            lesson_id=lesson_id,
            status='completed',
            time_spent=time_spent
        )
    
    @staticmethod
    def get_student_progress(student):
        """Get all progress records for a student"""
        try:
            progress_records = Progress.objects.filter(
                student=student
            ).select_related('lesson', 'lesson__course')
            return {'success': True, 'progress': progress_records}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_completed_count(student):
        """Get total completed lessons count for a student"""
        try:
            count = Progress.objects.filter(
                student=student,
                status='completed'
            ).count()
            return {'success': True, 'count': count}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_total_time_spent(student):
        """Get total time spent by student across all lessons"""
        try:
            total_time = Progress.objects.filter(
                student=student
            ).aggregate(total=Sum('time_spent_minutes'))['total'] or 0
            return {'success': True, 'total_time': total_time}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_courses_in_progress_count(student):
        """Get count of courses student has progress in"""
        try:
            count = Progress.objects.filter(
                student=student
            ).values('lesson__course').distinct().count()
            return {'success': True, 'count': count}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_student_overall_stats(student):
        """Get overall statistics for a student"""
        try:
            # Import CourseService here to avoid circular import
            from courses.services.CourseService import CourseService
            
            # Get completed count
            completed_result = ProgressService.get_completed_count(student)
            if not completed_result['success']:
                return completed_result
            completed_count = completed_result['count']
            
            # Get total time
            time_result = ProgressService.get_total_time_spent(student)
            if not time_result['success']:
                return time_result
            total_time = time_result['total_time']
            
            # Get courses in progress
            courses_result = ProgressService.get_courses_in_progress_count(student)
            if not courses_result['success']:
                return courses_result
            courses_in_progress = courses_result['count']
            
            # Get total published lessons from CourseService
            total_lessons_result = CourseService.get_total_published_lessons_count()
            if not total_lessons_result['success']:
                return total_lessons_result
            total_published_lessons = total_lessons_result['count']
            
            # Calculate overall progress
            overall_progress = (
                (completed_count / total_published_lessons * 100) 
                if total_published_lessons > 0 else 0
            )
            
            return {
                'success': True,
                'stats': {
                    'total_lessons_completed': completed_count,
                    'total_time_minutes': total_time,
                    'courses_in_progress': courses_in_progress,
                    'overall_progress_percentage': round(overall_progress, 2)
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_completed_lessons_for_course(student, course_id):
        """Get count of completed lessons for a specific course"""
        try:
            count = Progress.objects.filter(
                student=student,
                lesson__course_id=course_id,
                status='completed'
            ).count()
            return {'success': True, 'count': count}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_in_progress_count(student):
        """Get count of in-progress lessons"""
        try:
            count = Progress.objects.filter(
                student=student,
                status='in_progress'
            ).count()
            return {'success': True, 'count': count}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_progress_by_lesson(student, lesson_id):
        """Get progress for a specific lesson"""
        try:
            progress = Progress.objects.get(
                student=student,
                lesson_id=lesson_id
            )
            return {'success': True, 'progress': progress}
        except Progress.DoesNotExist:
            return {'success': False, 'error': 'Progress not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_time_spent_for_course(student, course_id):
        """Get total time spent on a course"""
        try:
            time_spent = Progress.objects.filter(
                student=student,
                lesson__course_id=course_id
            ).aggregate(total=Sum('time_spent_minutes'))['total'] or 0
            return {'success': True, 'time_spent': time_spent}
        except Exception as e:
            return {'success': False, 'error': str(e)}

