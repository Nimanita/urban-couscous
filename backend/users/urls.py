from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('me', views.get_current_user, name='current-user'),
    path('profile', views.update_profile, name='update-profile'),
    path('change-password', views.change_password, name='change-password'),
]