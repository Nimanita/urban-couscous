"""
courses/serializers.py - Course serializers
"""
from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Lesson serializer"""
    
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'course_title', 'title', 'description', 'content_type', 'order', 'estimated_minutes', 'created_at']
        read_only_fields = ['id', 'created_at']


class LessonWithProgressSerializer(serializers.Serializer):
    """Lesson with progress info"""
    
    id = serializers.IntegerField(source='lesson.id')
    title = serializers.CharField(source='lesson.title')
    description = serializers.CharField(source='lesson.description')
    content_type = serializers.CharField(source='lesson.content_type')
    order = serializers.IntegerField(source='lesson.order')
    estimated_minutes = serializers.IntegerField(source='lesson.estimated_minutes')
    status = serializers.CharField(source='progress.status')
    time_spent_minutes = serializers.IntegerField(source='progress.time_spent_minutes')
    completed_at = serializers.DateTimeField(source='progress.completed_at', allow_null=True)
    last_accessed = serializers.DateTimeField(source='progress.last_accessed', allow_null=True)
    notes = serializers.CharField(source='progress.notes', allow_blank=True)


class CourseSerializer(serializers.ModelSerializer):
    """Course serializer"""
    
    total_lessons = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'difficulty', 'estimated_hours', 'is_published', 'created_at', 'total_lessons']
        read_only_fields = ['id', 'created_at']
    
    def get_total_lessons(self, obj):
        return obj.lessons.count()


class CourseWithProgressSerializer(serializers.Serializer):
    """Course with progress info"""
    
    id = serializers.IntegerField(source='course.id')
    title = serializers.CharField(source='course.title')
    description = serializers.CharField(source='course.description')
    category = serializers.CharField(source='course.category')
    difficulty = serializers.CharField(source='course.difficulty')
    estimated_hours = serializers.IntegerField(source='course.estimated_hours')
    total_lessons = serializers.IntegerField()
    completed_lessons = serializers.IntegerField()
    progress_percentage = serializers.FloatField()
    time_spent_minutes = serializers.IntegerField()
    status = serializers.CharField()


class CourseDetailSerializer(serializers.ModelSerializer):
    """Course detail serializer with lessons"""
    
    lessons = LessonSerializer(many=True, read_only=True)
    total_lessons = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'difficulty', 'estimated_hours', 'is_published', 'created_at', 'total_lessons', 'lessons']
        read_only_fields = ['id', 'created_at']
    
    def get_total_lessons(self, obj):
        return obj.lessons.count()