from django.contrib import admin
from .models import Course, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['order', 'title', 'content_type', 'estimated_minutes']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'estimated_hours', 'is_published', 'created_at']
    list_filter = ['category', 'difficulty', 'is_published']
    search_fields = ['title', 'description']
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'content_type', 'order', 'estimated_minutes', 'created_at']
    list_filter = ['course', 'content_type']
    search_fields = ['title', 'description']
    ordering = ['course', 'order']
