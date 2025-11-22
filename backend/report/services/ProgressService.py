"""
progress/services.py - Progress tracking business logic
"""
from django.db import transaction
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from ..models import Progress


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
            progress_records = Progress.objects.filter(student=student).select_related('lesson', 'lesson__course')
            return {'success': True, 'progress': progress_records}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_student_overall_stats(student):
        """Get overall statistics for a student"""
        try:
            # Total lessons completed
            completed_count = Progress.objects.filter(
                student=student,
                status='completed'
            ).count()
            
            # Total time spent
            total_time = Progress.objects.filter(
                student=student
            ).aggregate(total=Sum('time_spent_minutes'))['total'] or 0
            
            # Courses in progress
            courses_in_progress = Progress.objects.filter(
                student=student
            ).values('lesson__course').distinct().count()
            
            # Overall progress percentage
            from courses.models import Lesson
            total_lessons = Lesson.objects.filter(course__is_published=True).count()
            overall_progress = (completed_count / total_lessons * 100) if total_lessons > 0 else 0
            
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

