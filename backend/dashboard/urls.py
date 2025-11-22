"""
dashboard/urls.py - Dashboard URL configuration
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.get_dashboard, name='main'),
    path('timeseries', views.get_time_series, name='timeseries'),
    path('distribution', views.get_completion_distribution, name='distribution'),
]