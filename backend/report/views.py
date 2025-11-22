"""
progress/views.py - Progress views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProgressSerializer, UpdateProgressSerializer
from .services.ProgressService import ProgressService
from .services.ActivityService import ActivityService

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_progress(request):
    """Get all progress for current student"""
    try:
        if request.user.role != 'student':
            return Response({
                'success': False,
                'error': 'Only students can access this endpoint'
            }, status=status.HTTP_403_FORBIDDEN)
        
        result = ProgressService.get_student_progress(request.user)
        
        if not result['success']:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProgressSerializer(result['progress'], many=True)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_progress(request):
    """Update progress for a lesson"""
    try:
        if request.user.role != 'student':
            return Response({
                'success': False,
                'error': 'Only students can update progress'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UpdateProgressSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        result = ProgressService.update_progress(
            student=request.user,
            lesson_id=serializer.validated_data['lesson_id'],
            status=serializer.validated_data.get('status'),
            time_spent=serializer.validated_data.get('time_spent'),
            notes=serializer.validated_data.get('notes')
        )
        
        if not result['success']:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        progress_serializer = ProgressSerializer(result['progress'])
        return Response({
            'success': True,
            'message': 'Progress updated successfully',
            'data': progress_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_lesson_complete(request, lesson_id):
    """Mark a lesson as complete"""
    try:
        if request.user.role != 'student':
            return Response({
                'success': False,
                'error': 'Only students can mark lessons complete'
            }, status=status.HTTP_403_FORBIDDEN)
        
        time_spent = request.data.get('time_spent', 0)
        
        result = ProgressService.mark_lesson_complete(
            student=request.user,
            lesson_id=lesson_id,
            time_spent=time_spent
        )
        
        if not result['success']:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProgressSerializer(result['progress'])
        return Response({
            'success': True,
            'message': 'Lesson marked as complete',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
