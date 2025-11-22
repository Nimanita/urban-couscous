"""
dashboard/views.py - Dashboard views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .service.DashboardService import DashboardService


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard(request):
    """Get dashboard data based on user role"""
    try:
        user = request.user
        
        if user.role == 'student':
            result = DashboardService.get_student_dashboard_data(user)
        elif user.role == 'mentor':
            result = DashboardService.get_mentor_dashboard_data()
        else:
            return Response({
                'success': False,
                'error': 'Invalid user role'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if not result['success']:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'success': True,
            'data': result['data']
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_time_series(request):
    """Get time series data for student"""
    try:
        if request.user.role != 'student':
            return Response({
                'success': False,
                'error': 'Only students can access this endpoint'
            }, status=status.HTTP_403_FORBIDDEN)
        
        days = int(request.query_params.get('days', 30))
        
        from report.services.ActivityService import ActivityService
        result = ActivityService.get_daily_time_series(request.user, days=days)
        
        if not result['success']:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'success': True,
            'data': result['data']
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_completion_distribution(request):
    """Get completion distribution for student"""
    try:
        if request.user.role != 'student':
            return Response({
                'success': False,
                'error': 'Only students can access this endpoint'
            }, status=status.HTTP_403_FORBIDDEN)
        
        result = DashboardService.get_completion_distribution(request.user)
        
        if not result['success']:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'success': True,
            'data': result['data']
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)