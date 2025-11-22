"""
dashboard/services.py - Dashboard business logic
"""
from django.db.models import Sum, Count, Q
from report.models import Progress , Activity , Recommendation
from courses.models import Course, Lesson
from report.services.ProgressService import ProgressService
from report.services.ActivityService import ActivityService
from report.services.RecommendationService import RecommendationService
class DashboardService:
    """Service class for dashboard operations"""
    
    @staticmethod
    def get_student_dashboard_data(student):
        """Get complete dashboard data for a student"""
        try:
            # Get overall stats
            stats_result = ProgressService.get_student_overall_stats(student)
            if not stats_result['success']:
                return stats_result
            
            stats = stats_result['stats']
            
            # Get time series data
            time_series_result = ActivityService.get_daily_time_series(student, days=30)
            if not time_series_result['success']:
                return time_series_result
            
            # Get course progress
            course_progress = DashboardService.get_course_progress_chart(student)
            if not course_progress['success']:
                return course_progress
            
            # Get completion distribution
            distribution = DashboardService.get_completion_distribution(student)
            if not distribution['success']:
                return distribution
            
            # Get learning streak
            streak_result = ActivityService.get_learning_streak(student)
            if not streak_result['success']:
                return streak_result
            
            existing_recs = Recommendation.objects.filter(
                student=student,
                is_dismissed=False
            ).count()
            
            if existing_recs == 0:
                RecommendationService.generate_recommendations(student)
            
            # Get recommendations
            recs_result = RecommendationService.get_active_recommendations(student)
            
            return {
                'success': True,
                'data': {
                    'summary': stats,
                    'time_series': time_series_result['data'],
                    'course_progress': course_progress['data'],
                    'completion_distribution': distribution['data'],
                    'learning_streak': streak_result['streak'],
                    'recommendations': recs_result['data'] if recs_result['success'] else []
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_course_progress_chart(student):
        """Get progress percentage for each course"""
        try:
            courses = Course.objects.filter(is_published=True).prefetch_related('lessons')
            
            data = []
            for course in courses:
                total_lessons = course.lessons.count()
                if total_lessons == 0:
                    continue
                
                completed_lessons = Progress.objects.filter(
                    student=student,
                    lesson__course=course,
                    status='completed'
                ).count()
                
                progress_percentage = round((completed_lessons / total_lessons) * 100, 2)
                
                data.append({
                    'course_id': course.id,
                    'course_name': course.title,
                    'progress': progress_percentage
                })
            
            return {'success': True, 'data': data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_completion_distribution(student):
        """Get distribution of lesson statuses"""
        try:
            # Get all published lessons
            total_lessons = Lesson.objects.filter(course__is_published=True).count()
            
            # Get completed lessons
            completed = Progress.objects.filter(
                student=student,
                status='completed'
            ).count()
            
            # Get in progress lessons
            in_progress = Progress.objects.filter(
                student=student,
                status='in_progress'
            ).count()
            
            # Calculate not started
            not_started = total_lessons - completed - in_progress
            
            data = [
                {'name': 'Completed', 'value': completed},
                {'name': 'In Progress', 'value': in_progress},
                {'name': 'Not Started', 'value': not_started}
            ]
            
            return {'success': True, 'data': data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_mentor_dashboard_data():
        """Get dashboard data for mentors"""
        try:
            from users.models import User
            
            students = User.objects.filter(role='student', is_active=True)
            
            student_data = []
            for student in students:
                stats_result = ProgressService.get_student_overall_stats(student)
                if stats_result['success']:
                    student_data.append({
                        'student_id': student.id,
                        'student_name': student.full_name,
                        'student_email': student.email,
                        'stats': stats_result['stats']
                    })
            
            # Calculate average completion rate
            if student_data:
                avg_completion = sum(s['stats']['overall_progress_percentage'] for s in student_data) / len(student_data)
            else:
                avg_completion = 0
            
            # Find students needing help (< 30% progress)
            students_needing_help = [s for s in student_data if s['stats']['overall_progress_percentage'] < 30]
            
            return {
                'success': True,
                'data': {
                    'total_students': len(student_data),
                    'average_completion_rate': round(avg_completion, 2),
                    'students': student_data,
                    'students_needing_help': students_needing_help
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}