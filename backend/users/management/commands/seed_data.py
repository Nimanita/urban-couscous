"""
Management command to seed database with sample data
Save as: users/management/commands/seed_data.py

Create the directories:
users/management/
users/management/commands/
users/management/__init__.py
users/management/commands/__init__.py
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import timedelta, datetime
import random

from users.models import User
from courses.models import Course, Lesson
from report.models import Progress, Activity


class Command(BaseCommand):
    help = 'Seed database with sample data for learning tracker'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data seeding...')
        
        try:
            with transaction.atomic():
                # Clear existing data
                self.stdout.write('Clearing existing data...')
                Activity.objects.all().delete()
                Progress.objects.all().delete()
                Lesson.objects.all().delete()
                Course.objects.all().delete()
                User.objects.filter(is_superuser=False).delete()
                
                # Create users
                self.stdout.write('Creating users...')
                users = self.create_users()
                
                # Create courses
                self.stdout.write('Creating courses...')
                courses = self.create_courses()
                
                # Create lessons
                self.stdout.write('Creating lessons...')
                self.create_lessons(courses)
                
                # Create progress data
                self.stdout.write('Creating progress data...')
                self.create_progress_data(users, courses)
                
                # Create activity data
                self.stdout.write('Creating activity data...')
                self.create_activity_data(users)
                
                self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding database: {str(e)}'))

    def create_users(self):
        """Create sample users"""
        users = {
            'alice': User.objects.create_user(
                email='alice@test.com',
                password='password123',
                first_name='Alice',
                last_name='Johnson',
                role='student'
            ),
            'bob': User.objects.create_user(
                email='bob@test.com',
                password='password123',
                first_name='Bob',
                last_name='Smith',
                role='student'
            ),
            'charlie': User.objects.create_user(
                email='charlie@test.com',
                password='password123',
                first_name='Charlie',
                last_name='Brown',
                role='student'
            ),
            'mentor': User.objects.create_user(
                email='mentor@test.com',
                password='password123',
                first_name='Sarah',
                last_name='Williams',
                role='mentor'
            ),
        }
        self.stdout.write(f'Created {len(users)} users')
        return users

    def create_courses(self):
        """Create sample courses"""
        courses = []
        
        course_data = [
            {
                'title': 'Python Fundamentals',
                'description': 'Learn the basics of Python programming including variables, data types, control flow, and functions.',
                'category': 'programming',
                'difficulty': 'beginner',
                'estimated_hours': 20
            },
            {
                'title': 'Web Development with Django',
                'description': 'Build modern web applications using Django framework. Learn models, views, templates, and REST APIs.',
                'category': 'web_development',
                'difficulty': 'intermediate',
                'estimated_hours': 30
            },
            {
                'title': 'Data Structures & Algorithms',
                'description': 'Master essential data structures and algorithms for technical interviews and problem-solving.',
                'category': 'programming',
                'difficulty': 'intermediate',
                'estimated_hours': 25
            },
            {
                'title': 'Machine Learning Basics',
                'description': 'Introduction to machine learning concepts, supervised and unsupervised learning, and practical implementations.',
                'category': 'machine_learning',
                'difficulty': 'advanced',
                'estimated_hours': 40
            },
        ]
        
        for data in course_data:
            course = Course.objects.create(**data)
            courses.append(course)
        
        self.stdout.write(f'Created {len(courses)} courses')
        return courses

    def create_lessons(self, courses):
        """Create lessons for each course"""
        
        # Python Fundamentals (20 lessons)
        python_lessons = [
            ('Introduction to Python', 'video', 30),
            ('Variables and Data Types', 'video', 45),
            ('Control Flow - If Statements', 'video', 60),
            ('Control Flow - Loops', 'video', 60),
            ('Functions Basics', 'video', 50),
            ('Lists and Tuples', 'video', 55),
            ('Dictionaries and Sets', 'video', 55),
            ('String Operations', 'reading', 40),
            ('File Handling', 'video', 50),
            ('Exception Handling', 'video', 45),
            ('Modules and Packages', 'reading', 40),
            ('Object-Oriented Programming', 'video', 70),
            ('Classes and Objects', 'video', 60),
            ('Inheritance', 'video', 55),
            ('Polymorphism', 'reading', 45),
            ('List Comprehensions', 'video', 40),
            ('Lambda Functions', 'video', 35),
            ('Decorators', 'video', 50),
            ('Generators', 'reading', 45),
            ('Final Project', 'exercise', 120),
        ]
        
        for i, (title, content_type, minutes) in enumerate(python_lessons, 1):
            Lesson.objects.create(
                course=courses[0],
                title=title,
                description=f'Learn about {title.lower()}',
                content_type=content_type,
                order=i,
                estimated_minutes=minutes
            )
        
        # Django (25 lessons)
        django_lessons = [
            ('Django Setup', 'video', 20),
            ('Project Structure', 'video', 30),
            ('Models and Databases', 'video', 90),
            ('Migrations', 'video', 45),
            ('Admin Interface', 'video', 40),
            ('URL Routing', 'video', 50),
            ('Views - Function Based', 'video', 60),
            ('Views - Class Based', 'video', 70),
            ('Templates', 'video', 60),
            ('Template Inheritance', 'video', 45),
            ('Static Files', 'reading', 40),
            ('Forms', 'video', 80),
            ('Model Forms', 'video', 65),
            ('User Authentication', 'video', 90),
            ('Permissions', 'video', 55),
            ('REST Framework Setup', 'video', 60),
            ('Serializers', 'video', 75),
            ('API Views', 'video', 70),
            ('ViewSets and Routers', 'video', 65),
            ('Authentication Tokens', 'video', 60),
            ('Testing', 'reading', 80),
            ('Deployment', 'reading', 90),
            ('PostgreSQL Integration', 'video', 70),
            ('Celery Tasks', 'video', 85),
            ('Final Project', 'exercise', 180),
        ]
        
        for i, (title, content_type, minutes) in enumerate(django_lessons, 1):
            Lesson.objects.create(
                course=courses[1],
                title=title,
                description=f'Learn about {title.lower()}',
                content_type=content_type,
                order=i,
                estimated_minutes=minutes
            )
        
        # DSA (20 lessons)
        dsa_lessons = [
            ('Arrays Basics', 'video', 60),
            ('Array Algorithms', 'video', 75),
            ('Linked Lists', 'video', 80),
            ('Stacks', 'video', 55),
            ('Queues', 'video', 55),
            ('Hash Tables', 'video', 70),
            ('Trees Introduction', 'video', 65),
            ('Binary Search Trees', 'video', 80),
            ('Tree Traversal', 'video', 70),
            ('Heaps', 'video', 75),
            ('Graphs Introduction', 'video', 60),
            ('Graph Traversal', 'video', 85),
            ('Sorting Algorithms', 'video', 90),
            ('Searching Algorithms', 'video', 65),
            ('Dynamic Programming', 'video', 100),
            ('Greedy Algorithms', 'video', 80),
            ('Backtracking', 'video', 85),
            ('Recursion', 'video', 75),
            ('Time Complexity', 'reading', 60),
            ('Practice Problems', 'exercise', 120),
        ]
        
        for i, (title, content_type, minutes) in enumerate(dsa_lessons, 1):
            Lesson.objects.create(
                course=courses[2],
                title=title,
                description=f'Learn about {title.lower()}',
                content_type=content_type,
                order=i,
                estimated_minutes=minutes
            )
        
        # Machine Learning (30 lessons)
        ml_lessons = [
            ('Introduction to ML', 'video', 60),
            ('Python for ML', 'video', 90),
            ('NumPy Basics', 'video', 75),
            ('Pandas Basics', 'video', 80),
            ('Data Visualization', 'video', 70),
            ('Statistics Fundamentals', 'reading', 90),
            ('Linear Regression', 'video', 100),
            ('Logistic Regression', 'video', 95),
            ('Decision Trees', 'video', 85),
            ('Random Forests', 'video', 90),
            ('Support Vector Machines', 'video', 100),
            ('K-Nearest Neighbors', 'video', 75),
            ('Naive Bayes', 'video', 80),
            ('Clustering - K-Means', 'video', 85),
            ('Hierarchical Clustering', 'video', 80),
            ('Dimensionality Reduction', 'video', 90),
            ('Principal Component Analysis', 'video', 95),
            ('Model Evaluation', 'video', 85),
            ('Cross Validation', 'video', 75),
            ('Hyperparameter Tuning', 'video', 90),
            ('Neural Networks Intro', 'video', 100),
            ('Deep Learning Basics', 'video', 110),
            ('Convolutional Networks', 'video', 120),
            ('Recurrent Networks', 'video', 115),
            ('Natural Language Processing', 'video', 105),
            ('Feature Engineering', 'reading', 95),
            ('Model Deployment', 'video', 100),
            ('ML Pipeline', 'video', 90),
            ('Ethics in ML', 'reading', 60),
            ('Final Project', 'exercise', 240),
        ]
        
        for i, (title, content_type, minutes) in enumerate(ml_lessons, 1):
            Lesson.objects.create(
                course=courses[3],
                title=title,
                description=f'Learn about {title.lower()}',
                content_type=content_type,
                order=i,
                estimated_minutes=minutes
            )
        
        self.stdout.write('Created lessons for all courses')

    def create_progress_data(self, users, courses):
        """Create progress data for students"""
        
        # Alice - 80% overall progress
        alice_progress = [
            (courses[0], 18, 20),  # Python: 90%
            (courses[1], 15, 25),  # Django: 60%
            (courses[2], 12, 20),  # DSA: 60%
            (courses[3], 5, 30),   # ML: 17%
        ]
        
        # Bob - 50% overall progress
        bob_progress = [
            (courses[0], 15, 20),  # Python: 75%
            (courses[1], 10, 25),  # Django: 40%
            (courses[2], 8, 20),   # DSA: 40%
            (courses[3], 2, 30),   # ML: 7%
        ]
        
        # Charlie - 20% overall progress
        charlie_progress = [
            (courses[0], 8, 20),   # Python: 40%
            (courses[1], 2, 25),   # Django: 8%
            (courses[2], 1, 20),   # DSA: 5%
            (courses[3], 0, 30),   # ML: 0%
        ]
        
        progress_data = [
            (users['alice'], alice_progress),
            (users['bob'], bob_progress),
            (users['charlie'], charlie_progress),
        ]
        
        for student, course_progress in progress_data:
            for course, completed, total in course_progress:
                lessons = list(course.lessons.all().order_by('order')[:total])
                
                for i, lesson in enumerate(lessons):
                    if i < completed:
                        # Completed lesson
                        time_spent = lesson.estimated_minutes + random.randint(-10, 20)
                        Progress.objects.create(
                            student=student,
                            lesson=lesson,
                            status='completed',
                            time_spent_minutes=time_spent,
                            completed_at=timezone.now() - timedelta(days=random.randint(1, 60)),
                            last_accessed=timezone.now() - timedelta(days=random.randint(0, 7))
                        )
                    elif i == completed and random.random() > 0.5:
                        # In progress lesson
                        time_spent = random.randint(10, lesson.estimated_minutes - 10)
                        Progress.objects.create(
                            student=student,
                            lesson=lesson,
                            status='in_progress',
                            time_spent_minutes=time_spent,
                            last_accessed=timezone.now() - timedelta(days=random.randint(0, 3))
                        )
        
        self.stdout.write('Created progress data for students')

    def create_activity_data(self, users):
        """Create activity data for last 30 days"""
        
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        # Alice: 4-6 sessions/day, 60-120 min/day
        self.create_student_activities(users['alice'], start_date, end_date, 4, 6, 60, 120)
        
        # Bob: 2-3 sessions/day, 30-60 min/day
        self.create_student_activities(users['bob'], start_date, end_date, 2, 3, 30, 60)
        
        # Charlie: 1-2 sessions/day, 15-30 min/day
        self.create_student_activities(users['charlie'], start_date, end_date, 1, 2, 15, 30)
        
        self.stdout.write('Created activity data for students')

    def create_student_activities(self, student, start_date, end_date, min_sessions, max_sessions, min_minutes, max_minutes):
        """Create activities for a student"""
        
        current_date = start_date
        while current_date <= end_date:
            # Reduce activity on weekends
            if current_date.weekday() >= 5:  # Saturday or Sunday
                if random.random() > 0.6:
                    current_date += timedelta(days=1)
                    continue
            
            # Random number of sessions
            num_sessions = random.randint(min_sessions, max_sessions)
            
            for _ in range(num_sessions):
                duration = random.randint(min_minutes, max_minutes)
                
                # Random time during the day
                hour = random.randint(7, 22)
                minute = random.randint(0, 59)
                
                timestamp = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=hour, minutes=minute)
                
                # Get a random lesson from completed progress
                progress_records = Progress.objects.filter(student=student, status__in=['completed', 'in_progress'])
                if progress_records.exists():
                    progress = random.choice(progress_records)
                    lesson = progress.lesson
                else:
                    lesson = None
                
                Activity.objects.create(
                    student=student,
                    lesson=lesson,
                    event_type=random.choice(['lesson_start', 'lesson_complete', 'session_start', 'session_end']),
                    duration_minutes=duration,
                    timestamp=timezone.make_aware(timestamp),
                    date=current_date
                )
            
            current_date += timedelta(days=1)