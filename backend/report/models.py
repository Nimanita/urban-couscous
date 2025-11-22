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
        ordering = ['-priority', '-created_at']