"""
courses/urls.py - Course URL configuration
"""
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.get_all_courses, name='list'),
    path('<int:course_id>', views.get_course_detail, name='detail'),
    path('<int:course_id>/lessons', views.get_course_lessons, name='lessons'),
]