from django.db import models
from django.utils import timezone
from users.models import User
from courses.models import Lesson


class Progress(models.Model):
    """Student progress tracking"""
    
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_records')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started', db_index=True)
    time_spent_minutes = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'progress'
        ordering = ['-last_accessed']
        unique_together = [['student', 'lesson']]
        indexes = [
            # Reason: filter Progress.objects.filter(student=student, status='completed')
            # Used in: get_completed_count, get_student_overall_stats_optimized, recommendation engine
            models.Index(fields=['student', 'status']),
            
            # Reason: filter Progress.objects.filter(student=student, lesson__course=course, status='completed')
            # Used in: get_completed_lessons_for_course, _recommend_course_gaps, _recommend_next_lessons
            models.Index(fields=['lesson', 'status']),
            
            # Reason: order by '-last_accessed' in _recommend_in_progress
            # Used in: RecommendationService._recommend_in_progress()
            models.Index(fields=['student', '-last_accessed']),
        ]
    
    def __str__(self):
        return f"{self.student.email} - {self.lesson.title}"


class Activity(models.Model):
    """Student activity tracking"""
    
    EVENT_TYPE_CHOICES = [
        ('lesson_start', 'Lesson Start'),
        ('lesson_complete', 'Lesson Complete'),
        ('session_start', 'Session Start'),
        ('session_end', 'Session End'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, db_index=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    date = models.DateField(default=timezone.now, db_index=True)
    
    class Meta:
        db_table = 'activities'
        ordering = ['-timestamp']

        indexes = [
            # Reason: filter Activity.objects.filter(student=student, date__gte=start_date)
            # Used in: get_daily_time_series (30-day chart), get_learning_streak
            models.Index(fields=['student', 'date']),
            
            # Reason: filter Activity.objects.filter(student=student, timestamp__gte=...)
            # Used in: get_recent_course_activity (last 7 days)
            models.Index(fields=['student', 'timestamp']),
        ]
         
    def __str__(self):
        return f"{self.student.email} - {self.event_type}"



class Recommendation(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE)
    reason = models.TextField()  # Why this is recommended
    priority = models.IntegerField(default=0)  # Higher = more important
    created_at = models.DateTimeField(auto_now_add=True)
    is_dismissed = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            # Reason: filter Recommendation.objects.filter(student=student, is_dismissed=False)
            # Used in: get_active_recommendations, dashboard endpoint
            models.Index(fields=['student', 'is_dismissed']),
        ]
         
        ordering = ['-priority', '-created_at']