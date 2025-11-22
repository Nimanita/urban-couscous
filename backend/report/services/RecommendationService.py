"""
report/services/RecommendationService.py - Adaptive recommendation logic
"""
"""
report/services/RecommendationService.py - Adaptive recommendation logic
"""
from django.db.models import Count, Avg, Q, F
from django.utils import timezone
from datetime import timedelta
from report.models import Progress, Activity, Recommendation
from courses.models import Lesson, Course

class RecommendationService:
    """Service for generating adaptive learning recommendations"""
    
    @staticmethod
    def generate_recommendations(student, limit=5):
        """
        Generate personalized recommendations based on:
        1. Current progress patterns
        2. Learning velocity
        3. Course completion gaps
        4. Time since last activity
        """
        try:
            recommendations = []
            
            # Clear old recommendations
            Recommendation.objects.filter(student=student).delete()
            
            # Strategy 1: Continue in-progress lessons
            in_progress_recs = RecommendationService.recommend_in_progress(student)
            recommendations.extend(in_progress_recs)
            
            # Strategy 2: Fill gaps in courses with high completion
            gap_recs = RecommendationService.recommend_course_gaps(student)
            recommendations.extend(gap_recs)
            
            # Strategy 3: Start next lesson in active courses
            next_lesson_recs = RecommendationService.recommend_next_lessons(student)
            recommendations.extend(next_lesson_recs)
            
            # Strategy 4: Revisit lessons with low time investment
            review_recs = RecommendationService.recommend_reviews(student)
            recommendations.extend(review_recs)
            
            # Strategy 5: Suggest new courses if current ones are going well
            new_course_recs = RecommendationService.recommend_new_courses(student)
            recommendations.extend(new_course_recs)
            
            # Strategy 6: If no recommendations yet, recommend starting first lessons
            if len(recommendations) == 0:
                beginner_recs = RecommendationService.recommend_beginner_courses(student)
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
    def recommend_in_progress(student):
        """Recommend lessons that are in progress (HIGH PRIORITY)"""
        recommendations = []
        
        try:
            in_progress = Progress.objects.filter(
                student=student,
                status='in_progress'
            ).select_related('lesson', 'lesson__course').order_by('-last_accessed')[:3]
            
            for progress in in_progress:
                days_since_access = (timezone.now() - progress.last_accessed).days
                
                # Higher priority if recently accessed
                priority = 90 - (days_since_access * 5)
                
                reason = f"You're {progress.time_spent_minutes} minutes into this lesson"
                if days_since_access > 3:
                    reason += f" (last accessed {days_since_access} days ago)"
                
                recommendations.append({
                    'lesson': progress.lesson,
                    'reason': reason,
                    'priority': max(priority, 70)  # Min priority 70
                })
        except Exception as e:
            pass
        
        return recommendations
    
    @staticmethod
    def recommend_course_gaps(student):
        """Recommend completing courses with >50% progress"""
        recommendations = []
        
        try:
            # Get courses with significant progress
            courses = Course.objects.filter(is_published=True).prefetch_related('lessons')
            
            for course in courses:
                total_lessons = course.lessons.count()
                if total_lessons == 0:
                    continue
                
                completed_count = Progress.objects.filter(
                    student=student,
                    lesson__course=course,
                    status='completed'
                ).count()
                
                progress_percentage = (completed_count / total_lessons) * 100
                
                # Recommend if progress is between 50% and 95%
                if 50 <= progress_percentage < 95:
                    # Find all lessons in this course
                    completed_lesson_ids = Progress.objects.filter(
                        student=student,
                        lesson__course=course,
                        status='completed'
                    ).values_list('lesson_id', flat=True)
                    
                    # Find next incomplete lesson in order
                    next_lesson = course.lessons.exclude(
                        id__in=completed_lesson_ids
                    ).order_by('order').first()
                    
                    if next_lesson:
                        priority = 60 + int(progress_percentage * 0.3)  # 60-88 range
                        
                        recommendations.append({
                            'lesson': next_lesson,
                            'reason': f"You're {progress_percentage:.0f}% through {course.title} - finish strong!",
                            'priority': priority
                        })
        except Exception as e:
            pass
        
        return recommendations
    
    @staticmethod
    def recommend_next_lessons(student):
        """Recommend next sequential lessons in active courses"""
        recommendations = []
        
        try:
            # Get courses where student has recent activity
            recent_activity = Activity.objects.filter(
                student=student,
                timestamp__gte=timezone.now() - timedelta(days=7)
            ).values_list('lesson__course_id', flat=True).distinct()
            
            active_courses = Course.objects.filter(
                id__in=recent_activity,
                is_published=True
            ).prefetch_related('lessons')
            
            for course in active_courses:
                # Get completed lesson IDs
                completed_lesson_ids = Progress.objects.filter(
                    student=student,
                    lesson__course=course,
                    status='completed'
                ).values_list('lesson_id', flat=True)
                
                # Find the first incomplete lesson
                next_lesson = course.lessons.exclude(
                    id__in=completed_lesson_ids
                ).order_by('order').first()
                
                if next_lesson:
                    # Check if previous lesson was completed
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
        except Exception as e:
            pass
        
        return recommendations
    
    @staticmethod
    def recommend_reviews(student):
        """Recommend reviewing lessons with low time investment"""
        recommendations = []
        
        try:
            # Find completed lessons with time spent < 50% of estimated time
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
        except Exception as e:
            pass
        
        return recommendations
    
    @staticmethod
    def recommend_new_courses(student):
        """Suggest new courses if student is doing well"""
        recommendations = []
        
        try:
            # Check if student has completed at least one course fully
            courses = Course.objects.filter(is_published=True).prefetch_related('lessons')
            
            for course in courses:
                total_lessons = course.lessons.count()
                if total_lessons == 0:
                    continue
                
                completed_count = Progress.objects.filter(
                    student=student,
                    lesson__course=course,
                    status='completed'
                ).count()
                
                # Check if course is 100% complete
                if completed_count == total_lessons:
                    # Find courses not started yet
                    started_course_ids = Progress.objects.filter(
                        student=student
                    ).values_list('lesson__course_id', flat=True).distinct()
                    
                    new_courses = Course.objects.filter(
                        is_published=True
                    ).exclude(id__in=started_course_ids).prefetch_related('lessons')[:2]
                    
                    for new_course in new_courses:
                        first_lesson = new_course.lessons.order_by('order').first()
                        if first_lesson:
                            recommendations.append({
                                'lesson': first_lesson,
                                'reason': f"Start a new challenge: {new_course.title}",
                                'priority': 30
                            })
                    break  # Only check once
        except Exception as e:
            pass
        
        return recommendations
    
    @staticmethod
    def recommend_beginner_courses(student):
        """Recommend beginner courses for new students"""
        recommendations = []
        
        try:
            # Get beginner courses
            beginner_courses = Course.objects.filter(
                is_published=True,
                difficulty='beginner'
            ).prefetch_related('lessons').order_by('id')[:3]
            
            for course in beginner_courses:
                first_lesson = course.lessons.order_by('order').first()
                if first_lesson:
                    recommendations.append({
                        'lesson': first_lesson,
                        'reason': f"Start your learning journey with {course.title}",
                        'priority': 85
                    })
            
            # If no beginner courses, recommend any first lessons
            if len(recommendations) == 0:
                all_courses = Course.objects.filter(
                    is_published=True
                ).prefetch_related('lessons').order_by('id')[:3]
                
                for course in all_courses:
                    first_lesson = course.lessons.order_by('order').first()
                    if first_lesson:
                        recommendations.append({
                            'lesson': first_lesson,
                            'reason': f"Begin with {course.title}",
                            'priority': 80
                        })
        except Exception as e:
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