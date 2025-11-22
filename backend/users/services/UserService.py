"""
users/services.py - User business logic
"""
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User


class UserService:
    """Service class for user operations"""
    
    @staticmethod
    def register_user(email, password, first_name, last_name, role='student'):
        """Register a new user"""
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    email=email.lower(),
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    role=role
                )
                return {'success': True, 'user': user}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def login_user(email, password):
        """Authenticate user and return tokens"""
        try:
            user = authenticate(username=email.lower(), password=password)
            
            if not user:
                return {'success': False, 'error': 'Invalid credentials'}
            
            if not user.is_active:
                return {'success': False, 'error': 'Account is disabled'}
            
            refresh = RefreshToken.for_user(user)
            
            return {
                'success': True,
                'user': user,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        try:
            user = User.objects.get(id=user_id)
            return {'success': True, 'user': user}
        except User.DoesNotExist:
            return {'success': False, 'error': 'User not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        try:
            user = User.objects.get(email=email.lower())
            return {'success': True, 'user': user}
        except User.DoesNotExist:
            return {'success': False, 'error': 'User not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """Update user information"""
        try:
            with transaction.atomic():
                user = User.objects.get(id=user_id)
                
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                
                user.save()
                return {'success': True, 'user': user}
        except User.DoesNotExist:
            return {'success': False, 'error': 'User not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def change_password(user, old_password, new_password):
        """Change user password"""
        try:
            if not user.check_password(old_password):
                return {'success': False, 'error': 'Old password is incorrect'}
            
            user.set_password(new_password)
            user.save()
            return {'success': True, 'message': 'Password changed successfully'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_all_students():
        """Get all students"""
        try:
            students = User.objects.filter(role='student', is_active=True).order_by('-created_at')
            return {'success': True, 'students': students}
        except Exception as e:
            return {'success': False, 'error': str(e)}