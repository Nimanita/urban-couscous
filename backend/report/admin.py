from django.contrib import admin
from .models import Progress, Activity, Recommendation


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'status', 'time_spent_minutes', 'completed_at', 'last_accessed']
    list_filter = ['status', 'completed_at']
    search_fields = ['student__email', 'lesson__title']
    raw_id_fields = ['student', 'lesson']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'event_type', 'duration_minutes', 'date', 'timestamp']
    list_filter = ['event_type', 'date']
    search_fields = ['student__email', 'lesson__title']
    raw_id_fields = ['student', 'lesson']
    date_hierarchy = 'date'


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'priority', 'is_viewed', 'is_accepted', 'created_at']
    list_filter = ['priority', 'is_viewed', 'is_accepted']
    search_fields = ['student__email', 'lesson__title', 'reason']
    raw_id_fields = ['student', 'lesson']
