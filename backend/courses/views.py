"""
courses/views.py - Course views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import CourseSerializer, CourseWithProgressSerializer, CourseDetailSerializer, LessonWithProgressSerializer
from .services.CourseService import CourseService
from .services.LessonService import LessonService


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_courses(request):
    """Get all courses with student progress"""
    try:
        user = request.user
        
        if user.role == 'student':
            result = CourseService.get_courses_with_student_progress(user)
            if not result['success']:
                return Response({
                    'success': False,
                    'error': result['error']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = CourseWithProgressSerializer(result['data'], many=True)
        else:
            result = CourseService.get_all_courses()
            if not result['success']:
                return Response({
                    'success': False,
                    'error': result['error']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = CourseSerializer(result['courses'], many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course_detail(request, course_id):
    """Get course detail by ID"""
    try:
        result = CourseService.get_course_by_id(course_id)
        
        if not result['success']:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CourseDetailSerializer(result['course'])
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course_lessons(request, course_id):
    """Get all lessons for a course with student progress"""
    try:
        user = request.user
        
        if user.role == 'student':
            result = LessonService.get_lessons_by_course(course_id, student=user)
            if not result['success']:
                return Response({
                    'success': False,
                    'error': result['error']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = LessonWithProgressSerializer(result['data'], many=True)
        else:
            result = LessonService.get_lessons_by_course(course_id)
            if not result['success']:
                return Response({
                    'success': False,
                    'error': result['error']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            from .serializers import LessonSerializer
            serializer = LessonSerializer(result['lessons'], many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)