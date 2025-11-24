"""
dashboard/services/DashboardService.py - Dashboard business logic
"""
from report.models import Recommendation


class DashboardService:
    """Service class for dashboard operations"""
    
    @staticmethod
    def get_student_dashboard_data(student):
        """Get complete dashboard data for a student"""
        try:
            # Import services here to avoid circular import
            from report.services.ProgressService import ProgressService
            from report.services.ActivityService import ActivityService
            from report.services.RecommendationService import RecommendationService
            
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
            
            # Check and generate recommendations if needed
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
            # Import services here to avoid circular import
            from courses.services.CourseService import CourseService
            from report.services.ProgressService import ProgressService
            
            # Get all courses with lesson counts
            courses_result = CourseService.get_courses_with_lesson_counts()
            if not courses_result['success']:
                return courses_result
            
            data = []
            for course_data in courses_result['data']:
                course = course_data['course']
                total_lessons = course_data['total_lessons']
                
                if total_lessons == 0:
                    continue
                
                # Get completed lessons from ProgressService
                completed_result = ProgressService.get_completed_lessons_for_course(
                    student,
                    course.id
                )
                
                if not completed_result['success']:
                    continue
                
                completed_lessons = completed_result['count']
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
            # Import services here to avoid circular import
            from courses.services.CourseService import CourseService
            from report.services.ProgressService import ProgressService
            
            # Get total published lessons
            total_lessons_result = CourseService.get_total_published_lessons_count()
            if not total_lessons_result['success']:
                return total_lessons_result
            
            total_lessons = total_lessons_result['count']
            
            # Get completed lessons
            completed_result = ProgressService.get_completed_count(student)
            if not completed_result['success']:
                return completed_result
            
            completed = completed_result['count']
            
            # Get in progress lessons
            in_progress_result = ProgressService.get_in_progress_count(student)
            if not in_progress_result['success']:
                return in_progress_result
            
            in_progress = in_progress_result['count']
            
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
            # Import services here to avoid circular import
            from users.services.UserService import UserService
            from report.services.ProgressService import ProgressService
            from courses.services.CourseService import CourseService
            
            # Get all students
            students_result = UserService.get_all_students()
            if not students_result['success']:
                return students_result
            
            students = students_result['students']
            
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
                avg_completion = sum(
                    s['stats']['overall_progress_percentage'] for s in student_data
                ) / len(student_data)
            else:
                avg_completion = 0
            
            # Find students needing help (< 30% progress)
            students_needing_help = [
                s for s in student_data 
                if s['stats']['overall_progress_percentage'] < 30
            ]
            
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