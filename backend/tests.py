from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from courses.models import Course, Lesson
from report.models import Progress, Activity, Recommendation
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()


# ============================================================================
# USER SERVICE TESTS
# ============================================================================

class UserServiceTests(TestCase):
    """Test User Service functionality"""
    
    def setUp(self):
        """Setup test data"""
        self.test_email = "testuser@example.com"
        self.test_password = "testpass123"
        
    def test_create_user(self):
        """Test creating a new user"""
        user = User.objects.create_user(
            email=self.test_email,
            password=self.test_password,
            first_name="Test",
            last_name="User",
            role="student"
        )
        self.assertEqual(user.email, self.test_email)
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.role, "student")
        self.assertTrue(user.is_active)
        
    def test_user_password_is_hashed(self):
        """Test that password is properly hashed"""
        user = User.objects.create_user(
            email=self.test_email,
            password=self.test_password,
            first_name="Test",
            last_name="User"
        )
        self.assertNotEqual(user.password, self.test_password)
        self.assertTrue(user.check_password(self.test_password))
        
    def test_create_student_user(self):
        """Test creating a student user"""
        user = User.objects.create_user(
            email="student@test.com",
            password="password123",
            first_name="Student",
            last_name="One",
            role="student"
        )
        self.assertEqual(user.role, "student")
        
    def test_create_mentor_user(self):
        """Test creating a mentor user"""
        user = User.objects.create_user(
            email="mentor@test.com",
            password="password123",
            first_name="Mentor",
            last_name="One",
            role="mentor"
        )
        self.assertEqual(user.role, "mentor")


# ============================================================================
# AUTHENTICATION API TESTS
# ============================================================================

class AuthenticationAPITests(APITestCase):
    """Test Authentication API endpoints"""
    
    def setUp(self):
        """Setup test client and data"""
        self.client = APIClient()
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"
        self.me_url = "/api/auth/me/"
        
    def test_register_student(self):
        """Test student registration"""
        data = {
            "email": "newstudent@test.com",
            "password": "password123",
            "first_name": "New",
            "last_name": "Student",
            "role": "student"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['email'], "newstudent@test.com")
        self.assertEqual(response.data['data']['role'], "student")
        
    def test_register_mentor(self):
        """Test mentor registration"""
        data = {
            "email": "newmentor@test.com",
            "password": "password123",
            "first_name": "New",
            "last_name": "Mentor",
            "role": "mentor"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['role'], "mentor")
        
    def test_login_success(self):
        """Test successful login"""
        # Create user first
        User.objects.create_user(
            email="logintest@test.com",
            password="password123",
            first_name="Login",
            last_name="Test"
        )
        
        # Try to login
        data = {
            "email": "logintest@test.com",
            "password": "password123"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('tokens', response.data['data'])
        self.assertIn('access', response.data['data']['tokens'])
        self.assertIn('refresh', response.data['data']['tokens'])
        
    def test_get_current_user(self):
        """Test getting current user info"""
        # Create and login user
        user = User.objects.create_user(
            email="currentuser@test.com",
            password="password123",
            first_name="Current",
            last_name="User"
        )
        self.client.force_authenticate(user=user)
        
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['email'], "currentuser@test.com")


# ============================================================================
# COURSE MODEL TESTS
# ============================================================================

class CourseModelTests(TestCase):
    """Test Course model"""
    
    def test_create_course(self):
        """Test creating a course"""
        course = Course.objects.create(
            title="Python Basics",
            description="Learn Python programming",
            category="programming",
            difficulty="beginner",
            estimated_hours=20,
            is_published=True
        )
        self.assertEqual(course.title, "Python Basics")
        self.assertEqual(course.category, "programming")
        self.assertEqual(course.difficulty, "beginner")
        self.assertTrue(course.is_published)
        
    def test_course_string_representation(self):
        """Test course string representation"""
        course = Course.objects.create(
            title="Django Web Dev",
            description="Build web apps",
            category="web_development",
            difficulty="intermediate",
            estimated_hours=30
        )
        self.assertEqual(str(course), "Django Web Dev")


# ============================================================================
# LESSON MODEL TESTS
# ============================================================================

class LessonModelTests(TestCase):
    """Test Lesson model"""
    
    def setUp(self):
        """Setup test course"""
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            category="programming",
            difficulty="beginner",
            estimated_hours=10
        )
        
    def test_create_lesson(self):
        """Test creating a lesson"""
        lesson = Lesson.objects.create(
            course=self.course,
            title="Introduction",
            description="Course introduction",
            content_type="video",
            order=1,
            estimated_minutes=30
        )
        self.assertEqual(lesson.title, "Introduction")
        self.assertEqual(lesson.course, self.course)
        self.assertEqual(lesson.content_type, "video")
        self.assertEqual(lesson.order, 1)
        
    def test_lesson_string_representation(self):
        """Test lesson string representation"""
        lesson = Lesson.objects.create(
            course=self.course,
            title="Python Variables",
            description="Learn about variables",
            content_type="video",
            order=2,
            estimated_minutes=45
        )
        self.assertEqual(str(lesson), "Python Variables")
        
    def test_multiple_lessons_in_course(self):
        """Test creating multiple lessons in a course"""
        lesson1 = Lesson.objects.create(
            course=self.course,
            title="Lesson 1",
            description="First lesson",
            content_type="video",
            order=1,
            estimated_minutes=30
        )
        lesson2 = Lesson.objects.create(
            course=self.course,
            title="Lesson 2",
            description="Second lesson",
            content_type="reading",
            order=2,
            estimated_minutes=45
        )
        self.assertEqual(self.course.lessons.count(), 2)


# ============================================================================
# COURSE API TESTS
# ============================================================================

class CourseAPITests(APITestCase):
    """Test Course API endpoints"""
    
    def setUp(self):
        """Setup test data"""
        self.client = APIClient()
        self.student = User.objects.create_user(
            email="student@test.com",
            password="password123",
            first_name="Student",
            last_name="User",
            role="student"
        )
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            category="programming",
            difficulty="beginner",
            estimated_hours=20,
            is_published=True
        )
        
    def test_get_all_courses_authenticated(self):
        """Test getting all courses as authenticated user"""
        self.client.force_authenticate(user=self.student)
        response = self.client.get("/api/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIsInstance(response.data['data'], list)
        
    def test_get_course_detail(self):
        """Test getting course detail"""
        self.client.force_authenticate(user=self.student)
        response = self.client.get(f"/api/courses/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['title'], "Test Course")
        
    def test_get_course_lessons(self):
        """Test getting course lessons"""
        # Create lessons
        Lesson.objects.create(
            course=self.course,
            title="Lesson 1",
            description="First lesson",
            content_type="video",
            order=1,
            estimated_minutes=30
        )
        Lesson.objects.create(
            course=self.course,
            title="Lesson 2",
            description="Second lesson",
            content_type="video",
            order=2,
            estimated_minutes=45
        )
        
        self.client.force_authenticate(user=self.student)
        response = self.client.get(f"/api/courses/{self.course.id}/lessons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 2)


# ============================================================================
# PROGRESS MODEL TESTS
# ============================================================================

class ProgressModelTests(TestCase):
    """Test Progress model"""
    
    def setUp(self):
        """Setup test data"""
        self.student = User.objects.create_user(
            email="student@test.com",
            password="password123",
            first_name="Student",
            last_name="User",
            role="student"
        )
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            category="programming",
            difficulty="beginner",
            estimated_hours=20
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            description="Test lesson description",
            content_type="video",
            order=1,
            estimated_minutes=30
        )
        
    def test_create_progress(self):
        """Test creating progress record"""
        progress = Progress.objects.create(
            student=self.student,
            lesson=self.lesson,
            status="not_started",
            time_spent_minutes=0
        )
        self.assertEqual(progress.student, self.student)
        self.assertEqual(progress.lesson, self.lesson)
        self.assertEqual(progress.status, "not_started")
        self.assertEqual(progress.time_spent_minutes, 0)
        
    def test_update_progress_to_in_progress(self):
        """Test updating progress to in_progress"""
        progress = Progress.objects.create(
            student=self.student,
            lesson=self.lesson,
            status="not_started"
        )
        progress.status = "in_progress"
        progress.time_spent_minutes = 15
        progress.save()
        
        self.assertEqual(progress.status, "in_progress")
        self.assertEqual(progress.time_spent_minutes, 15)
        
    def test_complete_lesson_progress(self):
        """Test marking lesson as complete"""
        progress = Progress.objects.create(
            student=self.student,
            lesson=self.lesson,
            status="in_progress",
            time_spent_minutes=20
        )
        progress.status = "completed"
        progress.completed_at = timezone.now()
        progress.time_spent_minutes = 35
        progress.save()
        
        self.assertEqual(progress.status, "completed")
        self.assertIsNotNone(progress.completed_at)
        self.assertEqual(progress.time_spent_minutes, 35)


# ============================================================================
# PROGRESS API TESTS
# ============================================================================

class ProgressAPITests(APITestCase):
    """Test Progress API endpoints"""
    
    def setUp(self):
        """Setup test data"""
        self.client = APIClient()
        self.student = User.objects.create_user(
            email="student@test.com",
            password="password123",
            first_name="Student",
            last_name="User",
            role="student"
        )
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            category="programming",
            difficulty="beginner",
            estimated_hours=20
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            description="Test Description",
            content_type="video",
            order=1,
            estimated_minutes=30
        )
        
    def test_get_student_progress(self):
        """Test getting student progress"""
        # Create progress
        Progress.objects.create(
            student=self.student,
            lesson=self.lesson,
            status="completed",
            time_spent_minutes=35
        )
        
        self.client.force_authenticate(user=self.student)
        response = self.client.get("/api/report/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIsInstance(response.data['data'], list)
        
    def test_update_progress(self):
        """Test updating progress"""
        self.client.force_authenticate(user=self.student)
        data = {
            "lesson_id": self.lesson.id,
            "status": "in_progress",
            "time_spent": 15,
            "notes": "Great lesson!"
        }
        response = self.client.post("/api/report/update/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
    def test_mark_lesson_complete(self):
        """Test marking lesson as complete"""
        self.client.force_authenticate(user=self.student)
        data = {"time_spent": 45}
        response = self.client.post(
            f"/api/report/complete/{self.lesson.id}/",
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['status'], "completed")


# ============================================================================
# ACTIVITY MODEL TESTS
# ============================================================================

class ActivityModelTests(TestCase):
    """Test Activity model"""
    
    def setUp(self):
        """Setup test data"""
        self.student = User.objects.create_user(
            email="student@test.com",
            password="password123",
            first_name="Student",
            last_name="User",
            role="student"
        )
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            category="programming",
            difficulty="beginner",
            estimated_hours=20
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            description="Test Description",
            content_type="video",
            order=1,
            estimated_minutes=30
        )
        
    def test_create_activity(self):
        """Test creating activity record"""
        activity = Activity.objects.create(
            student=self.student,
            lesson=self.lesson,
            event_type="lesson_start",
            duration_minutes=30,
            date=timezone.now().date()
        )
        self.assertEqual(activity.student, self.student)
        self.assertEqual(activity.lesson, self.lesson)
        self.assertEqual(activity.event_type, "lesson_start")
        self.assertEqual(activity.duration_minutes, 30)
        
    def test_create_lesson_complete_activity(self):
        """Test creating lesson complete activity"""
        activity = Activity.objects.create(
            student=self.student,
            lesson=self.lesson,
            event_type="lesson_complete",
            duration_minutes=45,
            date=timezone.now().date()
        )
        self.assertEqual(activity.event_type, "lesson_complete")
        self.assertEqual(activity.duration_minutes, 45)


# ============================================================================
# DASHBOARD API TESTS
# ============================================================================

class DashboardAPITests(APITestCase):
    """Test Dashboard API endpoints"""
    
    def setUp(self):
        """Setup test data"""
        self.client = APIClient()
        self.student = User.objects.create_user(
            email="student@test.com",
            password="password123",
            first_name="Student",
            last_name="User",
            role="student"
        )
        self.mentor = User.objects.create_user(
            email="mentor@test.com",
            password="password123",
            first_name="Mentor",
            last_name="User",
            role="mentor"
        )
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            category="programming",
            difficulty="beginner",
            estimated_hours=20,
            is_published=True
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            description="Test Description",
            content_type="video",
            order=1,
            estimated_minutes=30
        )
        
    def test_get_student_dashboard(self):
        """Test getting student dashboard"""
        # Create some progress
        Progress.objects.create(
            student=self.student,
            lesson=self.lesson,
            status="completed",
            time_spent_minutes=35
        )
        
        self.client.force_authenticate(user=self.student)
        response = self.client.get("/api/dashboard/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('summary', response.data['data'])
        self.assertIn('time_series', response.data['data'])
        self.assertIn('course_progress', response.data['data'])
        
    def test_get_mentor_dashboard(self):
        """Test getting mentor dashboard"""
        self.client.force_authenticate(user=self.mentor)
        response = self.client.get("/api/dashboard/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('total_students', response.data['data'])
        self.assertIn('students', response.data['data'])
        
    def test_get_timeseries_data(self):
        """Test getting time series data"""
        # Create activity
        Activity.objects.create(
            student=self.student,
            lesson=self.lesson,
            event_type="lesson_complete",
            duration_minutes=45,
            date=timezone.now().date()
        )
        
        self.client.force_authenticate(user=self.student)
        response = self.client.get("/api/dashboard/timeseries/?days=7")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIsInstance(response.data['data'], list)
        
    def test_get_completion_distribution(self):
        """Test getting completion distribution"""
        self.client.force_authenticate(user=self.student)
        response = self.client.get("/api/dashboard/distribution/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIsInstance(response.data['data'], list)


# ============================================================================
# RECOMMENDATION TESTS
# ============================================================================

class RecommendationModelTests(TestCase):
    """Test Recommendation model"""
    
    def setUp(self):
        """Setup test data"""
        self.student = User.objects.create_user(
            email="student@test.com",
            password="password123",
            first_name="Student",
            last_name="User",
            role="student"
        )
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            category="programming",
            difficulty="beginner",
            estimated_hours=20
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            description="Test Description",
            content_type="video",
            order=1,
            estimated_minutes=30
        )
        
    def test_create_recommendation(self):
        """Test creating a recommendation"""
        recommendation = Recommendation.objects.create(
            student=self.student,
            lesson=self.lesson,
            reason="Continue your progress",
            priority=90
        )
        self.assertEqual(recommendation.student, self.student)
        self.assertEqual(recommendation.lesson, self.lesson)
        self.assertEqual(recommendation.priority, 90)
        self.assertFalse(recommendation.is_dismissed)
        
    def test_dismiss_recommendation(self):
        """Test dismissing a recommendation"""
        recommendation = Recommendation.objects.create(
            student=self.student,
            lesson=self.lesson,
            reason="Start this lesson",
            priority=80
        )
        recommendation.is_dismissed = True
        recommendation.save()
        self.assertTrue(recommendation.is_dismissed)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class IntegrationTests(APITestCase):
    """Test complete workflows"""
    
    def setUp(self):
        """Setup complete test environment"""
        self.client = APIClient()
        
    def test_complete_student_workflow(self):
        """Test complete student registration to course completion"""
        # 1. Register student
        register_data = {
            "email": "newstudent@test.com",
            "password": "password123",
            "first_name": "New",
            "last_name": "Student",
            "role": "student"
        }
        register_response = self.client.post(
            "/api/auth/register/",
            register_data,
            format='json'
        )
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        
        # 2. Login
        login_data = {
            "email": "newstudent@test.com",
            "password": "password123"
        }
        login_response = self.client.post(
            "/api/auth/login/",
            login_data,
            format='json'
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token = login_response.data['data']['tokens']['access']
        
        # 3. Create a course and lesson
        course = Course.objects.create(
            title="Python Basics",
            description="Learn Python",
            category="programming",
            difficulty="beginner",
            estimated_hours=20,
            is_published=True
        )
        lesson = Lesson.objects.create(
            course=course,
            title="Introduction",
            description="Intro to Python",
            content_type="video",
            order=1,
            estimated_minutes=30
        )
        
        # 4. Get courses
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        courses_response = self.client.get("/api/courses/")
        self.assertEqual(courses_response.status_code, status.HTTP_200_OK)
        
        # 5. Update progress
        progress_data = {
            "lesson_id": lesson.id,
            "status": "in_progress",
            "time_spent": 15
        }
        progress_response = self.client.post(
            "/api/report/update/",
            progress_data,
            format='json'
        )
        self.assertEqual(progress_response.status_code, status.HTTP_200_OK)
        
        # 6. Mark lesson complete
        complete_data = {"time_spent": 30}
        complete_response = self.client.post(
            f"/api/report/complete/{lesson.id}/",
            complete_data,
            format='json'
        )
        self.assertEqual(complete_response.status_code, status.HTTP_200_OK)
        
        # 7. Check dashboard
        dashboard_response = self.client.get("/api/dashboard/")
        self.assertEqual(dashboard_response.status_code, status.HTTP_200_OK)
        self.assertGreater(
            dashboard_response.data['data']['summary']['total_lessons_completed'],
            0
        )
