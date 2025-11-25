"""
dashboard/services/DashboardService.py - Dashboard business logic (SUPER OPTIMIZED)
"""
from report.models import Recommendation
from courses.models import Course, Lesson


class DashboardService:
    """Service class for dashboard operations"""
    
    @staticmethod
    def get_student_dashboard_data(student):
        """Get complete dashboard data for a student (SUPER OPTIMIZED)"""
        try:
            from report.services.ProgressService import ProgressService
            from report.services.ActivityService import ActivityService
            from report.services.RecommendationService import RecommendationService
            
            # =================================================================
            # OPTIMIZATION 1: Single aggregation query for ALL stats
            # =================================================================
            stats_result = ProgressService.get_student_overall_stats_optimized(student)
            if not stats_result['success']:
                return stats_result
            
            summary = stats_result['stats']
            
            # =================================================================
            # OPTIMIZATION 2: Time series data (already optimized)
            # =================================================================
            time_series_result = ActivityService.get_daily_time_series(student, days=30)
            
            # =================================================================
            # OPTIMIZATION 3: Course progress with MINIMAL queries
            # =================================================================
            # Get all courses
            courses = Course.objects.filter(
                is_published=True
            ).prefetch_related('lessons')
            
            # Collect course IDs and lesson counts
            course_data = {}
            for course in courses:
                lesson_count = course.lessons.count()
                course_data[course.id] = {
                    'name': course.title,
                    'total_lessons': lesson_count
                }
            
            course_ids = list(course_data.keys())
            
            # Get all progress in ONE query using batch method
            progress_result = ProgressService.get_all_course_progress_batch(student, course_ids)
            if not progress_result['success']:
                return progress_result
            
            progress_stats = progress_result['stats']
            
            # Build course progress data
            course_progress_data = []
            for course_id, data in course_data.items():
                total_lessons = data['total_lessons']
                if total_lessons == 0:
                    continue
                
                stats = progress_stats.get(course_id, {'completed_count': 0})
                completed = stats['completed_count']
                progress_pct = (completed / total_lessons * 100) if total_lessons > 0 else 0
                
                course_progress_data.append({
                    'course_id': course_id,
                    'course_name': data['name'],
                    'progress': round(progress_pct, 2)
                })
            
            # =================================================================
            # OPTIMIZATION 4: Completion distribution (use aggregated data)
            # =================================================================
            completed = summary['total_lessons_completed']
            in_progress = summary['total_in_progress']
            total_published = summary['total_published_lessons']
            not_started = total_published - completed - in_progress
            
            distribution_data = [
                {'name': 'Completed', 'value': completed},
                {'name': 'In Progress', 'value': in_progress},
                {'name': 'Not Started', 'value': not_started}
            ]
            
            # =================================================================
            # OPTIMIZATION 5: Learning streak
            # =================================================================
            streak_result = ActivityService.get_learning_streak(student)
            
            # =================================================================
            # OPTIMIZATION 6: Recommendations with select_related
            # =================================================================
            recommendations = Recommendation.objects.filter(
                student=student,
                is_dismissed=False
            ).select_related('lesson', 'lesson__course')
            
            if not recommendations.exists():
                RecommendationService.generate_recommendations(student)
                recommendations = Recommendation.objects.filter(
                    student=student,
                    is_dismissed=False
                ).select_related('lesson', 'lesson__course')
            
            recs_data = [{
                'id': rec.id,
                'lesson': {
                    'id': rec.lesson.id,
                    'title': rec.lesson.title,
                    'course_title': rec.lesson.course.title,
                    'estimated_minutes': rec.lesson.estimated_minutes
                },
                'reason': rec.reason,
                'priority': rec.priority,
                'created_at': rec.created_at
            } for rec in recommendations]
            
            return {
                'success': True,
                'data': {
                    'summary': {
                        'total_lessons_completed': summary['total_lessons_completed'],
                        'total_time_minutes': summary['total_time_minutes'],
                        'courses_in_progress': summary['courses_in_progress'],
                        'overall_progress_percentage': summary['overall_progress_percentage']
                    },
                    'time_series': time_series_result['data'] if time_series_result['success'] else [],
                    'course_progress': course_progress_data,
                    'completion_distribution': distribution_data,
                    'learning_streak': streak_result['streak'] if streak_result['success'] else 0,
                    'recommendations': recs_data
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_course_progress_chart(student):
        """Get progress percentage for each course (OPTIMIZED)"""
        try:
            from report.services.ProgressService import ProgressService
            
            # Get all courses
            courses = Course.objects.filter(
                is_published=True
            ).prefetch_related('lessons')
            
            # Build course data
            course_data = {}
            course_ids = []
            for course in courses:
                lesson_count = course.lessons.count()
                if lesson_count > 0:
                    course_data[course.id] = {
                        'name': course.title,
                        'total_lessons': lesson_count
                    }
                    course_ids.append(course.id)
            
            # Get all progress in one query
            progress_result = ProgressService.get_all_course_progress_batch(student, course_ids)
            if not progress_result['success']:
                return progress_result
            
            progress_stats = progress_result['stats']
            
            # Calculate progress percentages
            data = []
            for course_id, info in course_data.items():
                stats = progress_stats.get(course_id, {'completed_count': 0})
                completed = stats['completed_count']
                total = info['total_lessons']
                
                progress_percentage = round((completed / total) * 100, 2)
                
                data.append({
                    'course_id': course_id,
                    'course_name': info['name'],
                    'progress': progress_percentage
                })
            
            return {'success': True, 'data': data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_completion_distribution(student):
        """Get distribution of lesson statuses (OPTIMIZED)"""
        try:
            from report.services.ProgressService import ProgressService
            
            # Use the optimized stats method that already has this data
            stats_result = ProgressService.get_student_overall_stats_optimized(student)
            if not stats_result['success']:
                return stats_result
            
            stats = stats_result['stats']
            
            completed = stats['total_lessons_completed']
            in_progress = stats['total_in_progress']
            total = stats['total_published_lessons']
            not_started = total - completed - in_progress
            
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
        """Get dashboard data for mentors (OPTIMIZED)"""
        try:
            from users.services.UserService import UserService
            from report.services.ProgressService import ProgressService
            
            # Get all students
            students_result = UserService.get_all_students()
            if not students_result['success']:
                return students_result
            
            students = students_result['students']
            
            # Get stats for each student using optimized method
            student_data = []
            for student in students:
                stats_result = ProgressService.get_student_overall_stats_optimized(student)
                if stats_result['success']:
                    stats = stats_result['stats']
                    student_data.append({
                        'student_id': student.id,
                        'student_name': student.full_name,
                        'student_email': student.email,
                        'stats': {
                            'total_lessons_completed': stats['total_lessons_completed'],
                            'total_time_minutes': stats['total_time_minutes'],
                            'courses_in_progress': stats['courses_in_progress'],
                            'overall_progress_percentage': stats['overall_progress_percentage']
                        }
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