from django.db import models
from django.utils import timezone


class Course(models.Model):
    """Course model"""
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    CATEGORY_CHOICES = [
        ('programming', 'Programming'),
        ('data_science', 'Data Science'),
        ('web_development', 'Web Development'),
        ('machine_learning', 'Machine Learning'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    estimated_hours = models.PositiveIntegerField()
    is_published = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'courses'
        ordering = ['title']
    
    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Lesson model"""
    
    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('reading', 'Reading'),
        ('quiz', 'Quiz'),
        ('exercise', 'Exercise'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='video')
    order = models.PositiveIntegerField(default=0)
    estimated_minutes = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lessons'
        ordering = ['course', 'order']
        unique_together = [['course', 'order']]
        
        indexes = [
            # Reason: filter course.lessons.order_by('order')
            # Used in: get_lessons_by_course, recommendation engine (finding next lesson)
            models.Index(fields=['course', 'order']),
        ]
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"