"""
progress/urls.py - Progress URL configuration
"""
from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('', views.get_student_progress, name='list'),
    path('update', views.update_progress, name='update'),
    path('complete/<int:lesson_id>', views.mark_lesson_complete, name='complete'),
    path('recommendations/generate', views.generate_recommendations, name='generate_recommendations'),
    path('recommendations/<int:recommendation_id>/dismiss', views.dismiss_recommendation, name='dismiss_recommendation'),
    path('recommendations', views.get_recommendations, name='get_recommendations'),
   
]