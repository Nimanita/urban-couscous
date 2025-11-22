"""
progress/serializers.py - Progress serializers
"""
from rest_framework import serializers
from .models import Progress, Activity


class ProgressSerializer(serializers.ModelSerializer):
    """Progress serializer"""
    
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    course_title = serializers.CharField(source='lesson.course.title', read_only=True)
    
    class Meta:
        model = Progress
        fields = ['id', 'student', 'lesson', 'lesson_title', 'course_title', 'status', 'time_spent_minutes', 'completed_at', 'last_accessed', 'notes']
        read_only_fields = ['id', 'student', 'completed_at', 'last_accessed']


class UpdateProgressSerializer(serializers.Serializer):
    """Serializer for updating progress"""
    
    lesson_id = serializers.IntegerField(required=True)
    status = serializers.ChoiceField(choices=['not_started', 'in_progress', 'completed'], required=False)
    time_spent = serializers.IntegerField(required=False, min_value=0)
    notes = serializers.CharField(required=False, allow_blank=True)


class ActivitySerializer(serializers.ModelSerializer):
    """Activity serializer"""
    
    class Meta:
        model = Activity
        fields = ['id', 'student', 'lesson', 'event_type', 'duration_minutes', 'timestamp', 'date']
        read_only_fields = ['id', 'student', 'timestamp', 'date']