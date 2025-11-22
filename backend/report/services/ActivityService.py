"""
progress/services.py - Progress tracking business logic
"""
from django.db import transaction
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from ..models import Activity


class ActivityService:
    """Service class for activity tracking"""
    
    @staticmethod
    def log_activity(student, event_type, lesson=None, duration_minutes=0):
        """Log a student activity"""
        try:
            activity = Activity.objects.create(
                student=student,
                lesson=lesson,
                event_type=event_type,
                duration_minutes=duration_minutes,
                date=timezone.now().date()
            )
            return {'success': True, 'activity': activity}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_daily_time_series(student, days=30):
        """Get daily learning time for last N days"""
        try:
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=days)
            
            activities = Activity.objects.filter(
                student=student,
                date__gte=start_date,
                date__lte=end_date
            ).values('date').annotate(
                total_minutes=Sum('duration_minutes')
            ).order_by('date')
            
            # Create a complete date range
            result = []
            current_date = start_date
            activities_dict = {act['date']: act['total_minutes'] for act in activities}
            
            while current_date <= end_date:
                result.append({
                    'date': current_date.isoformat(),
                    'minutes': activities_dict.get(current_date, 0)
                })
                current_date += timedelta(days=1)
            
            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_learning_streak(student):
        """Calculate current learning streak"""
        try:
            today = timezone.now().date()
            activities = Activity.objects.filter(
                student=student
            ).values('date').distinct().order_by('-date')
            
            if not activities:
                return {'success': True, 'streak': 0}
            
            streak = 0
            current_date = today
            
            for activity in activities:
                if activity['date'] == current_date:
                    streak += 1
                    current_date -= timedelta(days=1)
                elif activity['date'] == current_date - timedelta(days=1):
                    streak += 1
                    current_date = activity['date'] - timedelta(days=1)
                else:
                    break
            
            return {'success': True, 'streak': streak}
        except Exception as e:
            return {'success': False, 'error': str(e)}