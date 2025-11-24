"""
report/services/RecommendationService.py - Adaptive recommendation logic
"""
from django.db.models import F
from django.utils import timezone
from datetime import timedelta
from report.models import Progress, Recommendation


class RecommendationService:
    """Service for generating adaptive learning recommendations"""
    
    @staticmethod
    def generate_recommendations(student, limit=5):
        """Generate personalized recommendations based on learning patterns"""
        try:
            recommendations = []
            
            # Clear old recommendations
            Recommendation.objects.filter(student=student).delete()
            
            # Strategy 1: Continue in-progress lessons
            in_progress_recs = RecommendationService._recommend_in_progress(student)
            recommendations.extend(in_progress_recs)
            
            # Strategy 2: Fill gaps in courses with high completion
            gap_recs = RecommendationService._recommend_course_gaps(student)
            recommendations.extend(gap_recs)
            
            # Strategy 3: Start next lesson in active courses
            next_lesson_recs = RecommendationService._recommend_next_lessons(student)
            recommendations.extend(next_lesson_recs)
            
            # Strategy 4: Revisit lessons with low time investment
            review_recs = RecommendationService._recommend_reviews(student)
            recommendations.extend(review_recs)
            
            # Strategy 5: Suggest new courses if current ones are going well
            new_course_recs = RecommendationService._recommend_new_courses(student)
            recommendations.extend(new_course_recs)
            
            # Strategy 6: If no recommendations yet, recommend starting first lessons
            if len(recommendations) == 0:
                beginner_recs = RecommendationService._recommend_beginner_courses(student)
                recommendations.extend(beginner_recs)
            
            # Sort by priority and save top recommendations
            recommendations.sort(key=lambda x: x['priority'], reverse=True)
            
            saved_recommendations = []
            for rec in recommendations[:limit]:
                recommendation = Recommendation.objects.create(
                    student=student,
                    lesson=rec['lesson'],
                    reason=rec['reason'],
                    priority=rec['priority']
                )
                saved_recommendations.append(recommendation)
            
            return {
                'success': True,
                'recommendations': saved_recommendations,
                'count': len(saved_recommendations)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def _recommend_in_progress(student):
        """Recommend lessons that are in progress (HIGH PRIORITY)"""
        recommendations = []
        
        try:
            in_progress = Progress.objects.filter(
                student=student,
                status='in_progress'
            ).select_related('lesson', 'lesson__course').order_by('-last_accessed')[:3]
            
            for progress in in_progress:
                days_since_access = (timezone.now() - progress.last_accessed).days
                priority = 90 - (days_since_access * 5)
                
                reason = f"You're {progress.time_spent_minutes} minutes into this lesson"
                if days_since_access > 3:
                    reason += f" (last accessed {days_since_access} days ago)"
                
                recommendations.append({
                    'lesson': progress.lesson,
                    'reason': reason,
                    'priority': max(priority, 70)
                })
        except Exception:
            pass
        
        return recommendations
    
    @staticmethod
    def _recommend_course_gaps(student):
        """Recommend completing courses with >50% progress"""
        recommendations = []
        
        try:
            # Import CourseService here to avoid circular import
            from courses.services.CourseService import CourseService
            
            # Get all courses with lesson counts
            courses_result = CourseService.get_courses_with_lesson_counts()
            if not courses_result['success']:
                return recommendations
            
            for course_data in courses_result['data']:
                course = course_data['course']
                total_lessons = course_data['total_lessons']
                
                if total_lessons == 0:
                    continue
                
                completed_count = Progress.objects.filter(
                    student=student,
                    lesson__course=course,
                    status='completed'
                ).count()
                
                progress_percentage = (completed_count / total_lessons) * 100
                
                if 50 <= progress_percentage < 95:
                    completed_lesson_ids = Progress.objects.filter(
                        student=student,
                        lesson__course=course,
                        status='completed'
                    ).values_list('lesson_id', flat=True)
                    
                    next_lesson = course.lessons.exclude(
                        id__in=completed_lesson_ids
                    ).order_by('order').first()
                    
                    if next_lesson:
                        priority = 60 + int(progress_percentage * 0.3)
                        recommendations.append({
                            'lesson': next_lesson,
                            'reason': f"You're {progress_percentage:.0f}% through {course.title} - finish strong!",
                            'priority': priority
                        })
        except Exception:
            pass
        
        return recommendations
    
    @staticmethod
    def _recommend_next_lessons(student):
        """Recommend next sequential lessons in active courses"""
        recommendations = []
        
        try:
            # Import services here to avoid circular import
            from courses.services.CourseService import CourseService
            from report.services.ActivityService import ActivityService
            
            # Get recent course activity
            activity_result = ActivityService.get_recent_course_activity(student, days=7)
            if not activity_result['success']:
                return recommendations
            
            recent_course_ids = activity_result['course_ids']
            
            for course_id in recent_course_ids:
                course_result = CourseService.get_course_by_id(course_id)
                if not course_result['success']:
                    continue
                
                course = course_result['course']
                
                completed_lesson_ids = Progress.objects.filter(
                    student=student,
                    lesson__course=course,
                    status='completed'
                ).values_list('lesson_id', flat=True)
                
                next_lesson = course.lessons.exclude(
                    id__in=completed_lesson_ids
                ).order_by('order').first()
                
                if next_lesson:
                    prev_lessons = course.lessons.filter(
                        order__lt=next_lesson.order
                    ).order_by('-order')
                    
                    if prev_lessons.exists():
                        last_completed = Progress.objects.filter(
                            student=student,
                            lesson=prev_lessons.first(),
                            status='completed'
                        ).exists()
                        
                        if last_completed:
                            recommendations.append({
                                'lesson': next_lesson,
                                'reason': f"Next lesson in {course.title}",
                                'priority': 55
                            })
        except Exception:
            pass
        
        return recommendations
    
    @staticmethod
    def _recommend_reviews(student):
        """Recommend reviewing lessons with low time investment"""
        recommendations = []
        
        try:
            weak_lessons = Progress.objects.filter(
                student=student,
                status='completed',
                lesson__estimated_minutes__gt=0
            ).select_related('lesson').annotate(
                time_ratio=F('time_spent_minutes') * 100.0 / F('lesson__estimated_minutes')
            ).filter(time_ratio__lt=50).order_by('time_ratio')[:2]
            
            for progress in weak_lessons:
                recommendations.append({
                    'lesson': progress.lesson,
                    'reason': f"Quick review - you spent only {progress.time_spent_minutes}/{progress.lesson.estimated_minutes} min on this",
                    'priority': 40
                })
        except Exception:
            pass
        
        return recommendations
    
    @staticmethod
    def _recommend_new_courses(student):
        """Suggest new courses if student is doing well"""
        recommendations = []
        
        try:
            # Import CourseService here to avoid circular import
            from courses.services.CourseService import CourseService
            
            courses_result = CourseService.get_courses_with_lesson_counts()
            if not courses_result['success']:
                return recommendations
            
            for course_data in courses_result['data']:
                course = course_data['course']
                total_lessons = course_data['total_lessons']
                
                if total_lessons == 0:
                    continue
                
                completed_count = Progress.objects.filter(
                    student=student,
                    lesson__course=course,
                    status='completed'
                ).count()
                
                if completed_count == total_lessons:
                    started_course_ids = Progress.objects.filter(
                        student=student
                    ).values_list('lesson__course_id', flat=True).distinct()
                    
                    new_courses_result = CourseService.get_all_courses(is_published=True)
                    if new_courses_result['success']:
                        new_courses = [
                            c for c in new_courses_result['courses'] 
                            if c.id not in started_course_ids
                        ][:2]
                        
                        for new_course in new_courses:
                            first_lesson = new_course.lessons.order_by('order').first()
                            if first_lesson:
                                recommendations.append({
                                    'lesson': first_lesson,
                                    'reason': f"Start a new challenge: {new_course.title}",
                                    'priority': 30
                                })
                    break
        except Exception:
            pass
        
        return recommendations
    
    @staticmethod
    def _recommend_beginner_courses(student):
        """Recommend beginner courses for new students"""
        recommendations = []
        
        try:
            # Import CourseService here to avoid circular import
            from courses.services.CourseService import CourseService
            
            courses_result = CourseService.get_all_courses(is_published=True)
            if not courses_result['success']:
                return recommendations
            
            beginner_courses = [
                c for c in courses_result['courses'] 
                if hasattr(c, 'difficulty') and c.difficulty == 'beginner'
            ][:3]
            
            for course in beginner_courses:
                first_lesson = course.lessons.order_by('order').first()
                if first_lesson:
                    recommendations.append({
                        'lesson': first_lesson,
                        'reason': f"Start your learning journey with {course.title}",
                        'priority': 85
                    })
            
            if len(recommendations) == 0:
                all_courses = courses_result['courses'][:3]
                for course in all_courses:
                    first_lesson = course.lessons.order_by('order').first()
                    if first_lesson:
                        recommendations.append({
                            'lesson': first_lesson,
                            'reason': f"Begin with {course.title}",
                            'priority': 80
                        })
        except Exception:
            pass
        
        return recommendations
    
    @staticmethod
    def dismiss_recommendation(student, recommendation_id):
        """Allow students to dismiss recommendations"""
        try:
            recommendation = Recommendation.objects.get(
                id=recommendation_id,
                student=student
            )
            recommendation.is_dismissed = True
            recommendation.save()
            
            return {'success': True}
        except Recommendation.DoesNotExist:
            return {'success': False, 'error': 'Recommendation not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_active_recommendations(student):
        """Get non-dismissed recommendations for a student"""
        try:
            recommendations = Recommendation.objects.filter(
                student=student,
                is_dismissed=False
            ).select_related('lesson', 'lesson__course')
            
            data = [{
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
            
            return {'success': True, 'data': data}
        except Exception as e:
            return {'success': False, 'error': str(e)}