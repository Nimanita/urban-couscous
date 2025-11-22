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
from report.services.RecommendationService import RecommendationService

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    """
    GET /api/report/recommendations/
    Get personalized recommendations for the student
    """
    if request.user.role != 'student':
        return Response({
            'success': False,
            'error': 'Only students can get recommendations'
        }, status=status.HTTP_403_FORBIDDEN)
    
    result = RecommendationService.get_active_recommendations(request.user)
    
    if result['success']:
        return Response({
            'success': True,
            'data': result['data']
        })
    else:
        return Response({
            'success': False,
            'error': result['error']
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_recommendations(request):
    """
    POST /api/report/recommendations/generate/
    Generate new recommendations for the student
    """
    if request.user.role != 'student':
        return Response({
            'success': False,
            'error': 'Only students can generate recommendations'
        }, status=status.HTTP_403_FORBIDDEN)
    
    limit = request.data.get('limit', 5)
    result = RecommendationService.generate_recommendations(request.user, limit=limit)
    
    if result['success']:
        return Response({
            'success': True,
            'message': f'Generated {result["count"]} recommendations',
            'count': result['count']
        })
    else:
        return Response({
            'success': False,
            'error': result['error']
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dismiss_recommendation(request, recommendation_id):
    """
    POST /api/report/recommendations/{recommendation_id}/dismiss/
    Dismiss a recommendation
    """
    if request.user.role != 'student':
        return Response({
            'success': False,
            'error': 'Only students can dismiss recommendations'
        }, status=status.HTTP_403_FORBIDDEN)
    
    result = RecommendationService.dismiss_recommendation(request.user, recommendation_id)
    
    if result['success']:
        return Response({
            'success': True,
            'message': 'Recommendation dismissed'
        })
    else:
        return Response({
            'success': False,
            'error': result['error']
        }, status=status.HTTP_404_NOT_FOUND)

