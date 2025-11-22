# Learning Tracker - Progressive Student Dashboard

A comprehensive full-stack web application for tracking student learning progress across multiple courses with adaptive recommendations, role-based dashboards, and insightful analytics.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [API Documentation](#api-documentation)
- [Usage Guide](#usage-guide)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**Learning Tracker** is a modern, full-stack learning management system designed to help students track their progress across multiple courses while providing mentors with comprehensive oversight of student performance. The application features adaptive learning recommendations, detailed analytics, and an intuitive user interface.

### Key Highlights

- 📊 **Real-time Progress Tracking**: Monitor lesson completion, time spent, and course progress
- 🎯 **Adaptive Recommendations**: Smart AI-powered suggestions for next learning steps
- 👥 **Role-Based Access**: Separate dashboards for students and mentors
- 📈 **Rich Visualizations**: Interactive charts for time series data and completion statistics
- 🔐 **Secure Authentication**: JWT-based authentication system
- 📱 **Responsive Design**: Works seamlessly across desktop, tablet, and mobile devices

---

## ✨ Features

### Core Features

#### Authentication & Authorization
- ✅ Email-based authentication with JWT tokens
- ✅ Role-based access control (Student/Mentor)
- ✅ Secure password management
- ✅ Profile management

#### Student Dashboard
- ✅ Overview of completed lessons and time spent
- ✅ Progress tracking per course
- ✅ Time series trend chart (last 30 days)
- ✅ Completion distribution pie chart
- ✅ Learning streak counter
- ✅ Course catalog with real-time progress

#### Mentor Dashboard
- ✅ Overview of all students
- ✅ Average completion rate metrics
- ✅ Students needing help identification
- ✅ Individual student performance details

#### Progress Tracking
- ✅ Lesson-level progress (not started, in progress, completed)
- ✅ Time tracking per lesson
- ✅ Personal notes for each lesson
- ✅ Last accessed timestamps

### Stretch Features

#### Adaptive Recommendations
- ✅ Intelligent lesson suggestions based on:
  - Current progress patterns
  - Learning velocity
  - Course completion gaps
  - Time since last activity
- ✅ Priority-based recommendation system
- ✅ Dismissible recommendations

#### Data Visualization
- ✅ Interactive time series charts
- ✅ Donut charts for completion distribution
- ✅ Course progress bars
- ✅ Real-time data updates

#### Additional Features
- ✅ Activity logging and tracking
- ✅ Comprehensive API documentation
- ✅ Seeded sample data for testing
- ✅ Clear setup instructions
- ✅ Responsive UI design

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              React Frontend (Port 5173)                   │  │
│  │                                                            │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐  │  │
│  │  │   Auth     │  │  Dashboard │  │  Course Explorer │  │  │
│  │  │  Pages     │  │   Pages    │  │     Pages        │  │  │
│  │  └────────────┘  └────────────┘  └──────────────────┘  │  │
│  │                                                            │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │         Context API (Auth, Theme)                  │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │         Axios API Client                           │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ HTTP/HTTPS (REST API)
                            │ JWT Authentication
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                      APPLICATION LAYER                           │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Django REST Framework (Port 8000)              │  │
│  │                                                            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌─────────┐  ┌──────────┐ │  │
│  │  │  Users   │  │ Courses  │  │ Report  │  │Dashboard │ │  │
│  │  │   App    │  │   App    │  │   App   │  │   App    │ │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬────┘  └────┬─────┘ │  │
│  │       │             │              │             │        │  │
│  │  ┌────▼─────────────▼──────────────▼─────────────▼────┐ │  │
│  │  │              Service Layer                         │ │  │
│  │  │  • UserService                                     │ │  │
│  │  │  • CourseService / LessonService                  │ │  │
│  │  │  • ProgressService / ActivityService             │ │  │
│  │  │  • RecommendationService / DashboardService      │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                                                            │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │              Django ORM                            │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ SQL Queries
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                        DATA LAYER                                │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              PostgreSQL Database                          │  │
│  │                                                            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │  │
│  │  │  Users   │  │ Courses  │  │ Progress │  │Activity │ │  │
│  │  │  Table   │  │ & Lessons│  │  Table   │  │ Table   │ │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │  │
│  │                                                            │  │
│  │  ┌──────────────────┐                                     │  │
│  │  │ Recommendations  │                                     │  │
│  │  │      Table       │                                     │  │
│  │  └──────────────────┘                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
```

### Application Flow

```
┌─────────────┐
│   Student   │
│   Logs In   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│  JWT Token Generated    │
│  & Stored in Context    │
└──────────┬──────────────┘
           │
           ▼
┌────────────────────────────────────┐
│   Dashboard Loads                  │
│   • Fetches Progress Data          │
│   • Generates Recommendations      │
│   • Loads Time Series              │
│   • Calculates Streak              │
└──────────┬─────────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│   Student Interacts                │
│   • Views Courses                  │
│   • Completes Lessons              │
│   • Updates Progress               │
└──────────┬─────────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│   Backend Updates                  │
│   • Progress Records               │
│   • Activity Logs                  │
│   • Recommendation Engine          │
└────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **HTTP Client**: Axios
- **State Management**: React Context API
- **Routing**: React Router DOM

### Backend
- **Framework**: Django 4.2
- **API**: Django REST Framework
- **Authentication**: djangorestframework-simplejwt
- **Database**: PostgreSQL 12+
- **CORS**: django-cors-headers
- **Environment**: python-dotenv

### Development Tools
- **Version Control**: Git
- **Package Managers**: npm, pip
- **Code Quality**: ESLint, Python Black (optional)

---

## 📁 Project Structure

```
learning_tracker/
│
├── backend/                          # Django Backend
│   ├── config/                       # Project Configuration
│   │   ├── settings.py              # Django settings
│   │   ├── urls.py                  # Root URL configuration
│   │   ├── wsgi.py                  # WSGI configuration
│   │   └── asgi.py                  # ASGI configuration
│   │
│   ├── users/                        # User Management App
│   │   ├── models.py                # User model (custom with roles)
│   │   ├── serializers.py           # User serializers
│   │   ├── views.py                 # Authentication views
│   │   ├── urls.py                  # User endpoints
│   │   ├── services/                
│   │   │   └── UserService.py       # User business logic
│   │   └── management/
│   │       └── commands/
│   │           └── seed_data.py     # Database seeding
│   │
│   ├── courses/                      # Course Management App
│   │   ├── models.py                # Course & Lesson models
│   │   ├── serializers.py           # Course serializers
│   │   ├── views.py                 # Course views
│   │   ├── urls.py                  # Course endpoints
│   │   └── services/
│   │       ├── CourseService.py     # Course logic
│   │       └── LessonService.py     # Lesson logic
│   │
│   ├── report/                       # Progress Tracking App
│   │   ├── models.py                # Progress, Activity, Recommendation
│   │   ├── serializers.py           # Progress serializers
│   │   ├── views.py                 # Progress views
│   │   ├── urls.py                  # Progress endpoints
│   │   └── services/
│   │       ├── ProgressService.py   # Progress tracking
│   │       ├── ActivityService.py   # Activity logging
│   │       └── RecommendationService.py  # Adaptive recommendations
│   │
│   ├── dashboard/                    # Dashboard Analytics App
│   │   ├── views.py                 # Dashboard views
│   │   ├── urls.py                  # Dashboard endpoints
│   │   └── service/
│   │       └── DashboardService.py  # Dashboard logic
│   │
│   ├── manage.py                     # Django management script
│   ├── requirements.txt              # Python dependencies
│   └── .env                         # Environment variables
│
├── frontend/                         # React Frontend
│   ├── src/
│   │   ├── api/                     # API client configuration
│   │   │   └── axios.js             # Axios instance
│   │   │
│   │   ├── components/              # Reusable components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── CourseCard.jsx
│   │   │   ├── ProgressChart.jsx
│   │   │   └── ...
│   │   │
│   │   ├── pages/                   # Page components
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Courses.jsx
│   │   │   ├── CourseDetails.jsx
│   │   │   └── ...
│   │   │
│   │   ├── context/                 # React Context
│   │   │   └── AuthContext.jsx     # Authentication context
│   │   │
│   │   ├── utils/                   # Utility functions
│   │   │   └── helpers.js
│   │   │
│   │   ├── App.jsx                  # Main App component
│   │   ├── main.jsx                 # Entry point
│   │   └── index.css                # Global styles
│   │
│   ├── public/                       # Static assets
│   ├── package.json                  # npm dependencies
│   ├── vite.config.js               # Vite configuration
│   ├── tailwind.config.js           # Tailwind configuration
│   └── .env                         # Environment variables
│
├── README.md                         # This file
└── LICENSE                          # MIT License
```

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** and npm - [Download](https://nodejs.org/)
- **PostgreSQL 12+** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/downloads)

### Verify Installations

```bash
# Check Python version
python --version  # or python3 --version

# Check Node.js and npm versions
node --version
npm --version

# Check PostgreSQL version
psql --version

# Check Git version
git --version
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/learning-tracker.git
cd learning-tracker
```

### 2. Backend Setup

#### Step 2.1: Create Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv env

# Activate virtual environment
# On Linux/Mac:
source env/bin/activate

# On Windows:
env\Scripts\activate
```

#### Step 2.2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 2.3: Configure Database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE learning_tracker;

# Exit PostgreSQL
\q
```

#### Step 2.4: Setup Environment Variables

Create a `.env` file in the `backend/` directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=learning_tracker
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:5173
```

**Note**: Replace `your-postgres-password` with your actual PostgreSQL password.

#### Step 2.5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Step 2.6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

#### Step 2.7: Seed Database with Sample Data

```bash
python manage.py seed_data
```

This command creates:
- **3 Students**: alice@test.com, bob@test.com, charlie@test.com
- **1 Mentor**: mentor@test.com
- **4 Courses**: Python Fundamentals, Django Web Development, Data Structures & Algorithms, Machine Learning Basics
- **95 Total Lessons** across all courses
- **Progress data** for all students with varying completion rates
- **30 days of activity data**

**Default password for all users**: `password123`

#### Step 2.8: Start Backend Server

```bash
python manage.py runserver
```

Backend API will be available at: `http://localhost:8000`

---

### 3. Frontend Setup

Open a new terminal window/tab.

#### Step 3.1: Navigate to Frontend Directory

```bash
cd frontend
```

#### Step 3.2: Install Dependencies

```bash
npm install
```

#### Step 3.3: Configure Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000/api
```

#### Step 3.4: Start Development Server

```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

---

### 4. Access the Application

1. Open your browser and navigate to `http://localhost:5173`
2. Login with one of the seeded accounts:

**Student Accounts:**
- Email: `alice@test.com` | Password: `password123`
- Email: `bob@test.com` | Password: `password123`
- Email: `charlie@test.com` | Password: `password123`

**Mentor Account:**
- Email: `mentor@test.com` | Password: `password123`

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Authentication

All protected endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Endpoints Overview

#### Authentication Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/auth/register/` | Register new user | Public |
| POST | `/auth/login/` | Login user | Public |
| GET | `/auth/me/` | Get current user | Protected |
| PUT | `/auth/profile/` | Update profile | Protected |
| POST | `/auth/change-password/` | Change password | Protected |

#### Course Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/courses/` | List all courses with progress | Protected |
| GET | `/courses/{id}/` | Get course details | Protected |
| GET | `/courses/{id}/lessons/` | Get course lessons with progress | Protected |

#### Progress Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/report/` | Get student progress | Protected (Student) |
| POST | `/report/update/` | Update lesson progress | Protected (Student) |
| POST | `/report/complete/{lesson_id}/` | Mark lesson complete | Protected (Student) |

#### Dashboard Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/dashboard/` | Get dashboard data | Protected |
| GET | `/dashboard/timeseries/` | Get time series data | Protected (Student) |
| GET | `/dashboard/distribution/` | Get completion distribution | Protected (Student) |

### Sample API Requests

#### Login Request

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@test.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "email": "alice@test.com",
      "first_name": "Alice",
      "last_name": "Johnson",
      "role": "student"
    },
    "tokens": {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
  }
}
```

#### Get Dashboard Data

```bash
curl -X GET http://localhost:8000/api/dashboard/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Update Progress

```bash
curl -X POST http://localhost:8000/api/report/update/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "lesson_id": 1,
    "status": "completed",
    "time_spent": 45,
    "notes": "Great lesson!"
  }'
```

For complete API documentation, see [api_documentation.txt](backend/api_documentation.txt).

---

## 📖 Usage Guide

### For Students

#### 1. Dashboard Overview
- View your overall progress statistics
- See completed lessons and total time spent
- Check your learning streak
- View courses in progress

#### 2. Exploring Courses
- Browse available courses in the catalog
- View course details including difficulty and estimated time
- See your current progress for each course

#### 3. Taking Lessons
- Navigate to a course and select a lesson
- Mark lessons as "in progress" or "completed"
- Add personal notes for each lesson
- Track time spent on each lesson

#### 4. Viewing Analytics
- Check your 30-day learning time series chart
- View completion distribution (completed, in progress, not started)
- Monitor course-by-course progress

#### 5. Following Recommendations
- Review personalized lesson recommendations
- Recommendations adapt based on your learning patterns
- Dismiss recommendations you don't want to follow

### For Mentors

#### 1. Mentor Dashboard
- View all students and their progress
- See average completion rates
- Identify students who need help (< 30% progress)

#### 2. Student Monitoring
- Check individual student statistics
- Review time spent and lessons completed
- Monitor courses in progress per student

---

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ email           │
│ password        │
│ first_name      │
│ last_name       │
│ role            │◄──────────────┐
│ is_active       │               │
│ created_at      │               │
│ updated_at      │               │
└─────────────────┘               │
                                  │
                                  │
┌─────────────────┐               │
│     Course      │               │
├─────────────────┤               │
│ id (PK)         │               │
│ title           │               │
│ description     │               │
│ category        │               │
│ difficulty      │               │
│ estimated_hours │               │
│ is_published    │               │
│ created_at      │               │
│ updated_at      │               │
└────────┬────────┘               │
         │                        │
         │ 1:N                    │
         │                        │
┌────────▼────────┐               │
│     Lesson      │               │
├─────────────────┤               │
│ id (PK)         │               │
│ course_id (FK)  │               │
│ title           │               │
│ description     │               │
│ content_type    │               │
│ order           │               │
│ estimated_min   │               │
│ created_at      │               │
│ updated_at      │               │
└────────┬────────┘               │
         │                        │
         │ N:M via Progress       │
         │                        │
┌────────▼────────┐               │
│    Progress     │               │
├─────────────────┤               │
│ id (PK)         │               │
│ student_id (FK) │───────────────┘
│ lesson_id (FK)  │
│ status          │
│ time_spent_min  │
│ completed_at    │
│ last_accessed   │
│ notes           │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │
┌────────▼────────┐
│    Activity     │
├─────────────────┤
│ id (PK)         │
│ student_id (FK) │
│ lesson_id (FK)  │
│ event_type      │
│ duration_min    │
│ date            │
│ timestamp       │
└─────────────────┘

┌──────────────────┐
│ Recommendation   │
├──────────────────┤
│ id (PK)          │
│ student_id (FK)  │
│ lesson_id (FK)   │
│ reason           │
│ priority         │
│ is_dismissed     │
│ created_at       │
└──────────────────┘
```

### Key Models

#### User
- Custom user model with email authentication
- Roles: `student`, `mentor`
- Tracks active status and timestamps

#### Course
- Categories: programming, web_development, data_science, machine_learning, other
- Difficulty levels: beginner, intermediate, advanced
- Published status for visibility control

#### Lesson
- Belongs to a course
- Content types: video, reading, quiz, exercise
- Ordered sequentially within courses

#### Progress
- Links students to lessons
- Statuses: not_started, in_progress, completed
- Tracks time spent, completion date, and notes

#### Activity
- Logs all student learning activities
- Event types: lesson_start, lesson_complete, etc.
- Used for analytics and streak calculation

#### Recommendation
- Adaptive suggestions generated by AI algorithm
- Priority-based ranking
- Can be dismissed by students

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
python manage.py test
```

### Frontend Tests

```bash
cd frontend
npm run test
```

### Manual Testing Checklist

- [ ] User can register and login
- [ ] Dashboard loads with correct data
- [ ] Course catalog displays all courses
- [ ] Lessons can be marked as complete
- [ ] Progress updates reflect in real-time
- [ ] Time series chart shows accurate data
- [ ] Recommendations are generated
- [ ] Mentor dashboard shows all students
- [ ] API returns proper error messages
- [ ] Responsive design works on mobile

---

## 🚢 Deployment

### Backend Deployment (Django)

#### Preparation

1. **Update settings.py**:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')
```

2. **Collect static files**:
```bash
python manage.py collectstatic
```

3. **Update database settings for production**

#### Deployment Options

- **Heroku**: Use Gunicorn and PostgreSQL add-on
- **AWS EC2**: Deploy with Nginx and Gunicorn
- **DigitalOcean**: Use App Platform or Droplets
- **Railway**: Simple deployment with PostgreSQL

### Frontend Deployment (React)

#### Build Production Bundle

```bash
cd frontend
npm run build
```

#### Deployment Options

- **Vercel**: Automatic deployment from Git
- **Netlify**: Easy static site hosting
- **AWS S3 + CloudFront**: Scalable hosting
- **GitHub Pages**: Free hosting for static sites

### Deployment Checklist

- [ ] Set `DEBUG=False` in Django
- [ ] Update `SECRET_KEY` with strong random key
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up production database (PostgreSQL)
- [ ] Configure CORS properly
- [ ] Set up SSL/HTTPS certificates
- [ ] Configure static file serving
- [ ] Set up logging
- [ ] Configure backup strategy
- [ ] Update frontend API URL to production
- [ ] Enable rate limiting
- [ ] Set up monitoring (Sentry, etc.)

---

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'corsheaders'`
```bash
# Solution: Install django-cors-headers
pip install django-cors-headers
```

**Issue**: Database connection error
```bash
# Solution: Check PostgreSQL service is running
sudo service postgresql start  # Linux
brew services start postgresql  # Mac
```

**Issue**: Migration errors
```bash
# Solution: Reset migrations
python manage.py migrate --fake
python manage.py migrate
```

#### Frontend Issues

**Issue**: `Cannot find module` errors
```bash
# Solution: Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Issue**: CORS errors
```bash
# Solution: Check backend CORS_ALLOWED_ORIGINS includes frontend URL
# In backend .env:
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

**Issue**: API calls returning 401 Unauthorized
```bash
# Solution: Check JWT token is being sent correctly
# Verify AuthContext is providing token
# Check token expiration
```

### Debug Mode

Enable detailed error messages:

**Backend**:
```python
# settings.py
DEBUG = True
```

**Frontend**:
```javascript
// Add console logs in API calls
console.log('API Response:', response.data);
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add: your feature description"
   ```
4. **Push to your branch**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request**

### Coding Standards

- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Write meaningful commit messages
- Add comments for complex logic
- Write tests for new features
- Update documentation as needed

### Code Review Process

- All PRs require at least one review
- Ensure all tests pass before merging
- Update README if adding new features
- Keep PRs focused and atomic

---

## 📊 Sample Data Overview

The seeded database includes realistic test data:

### Students

| Name | Email | Progress | Notable Traits |
|------|-------|----------|----------------|
| Alice Johnson | alice@test.com | 80% | High achiever, consistent learner |
| Bob Smith | bob@test.com | 50% | Moderate pace, balanced progress |
| Charlie Brown | charlie@test.com | 20% | Needs help, slow starter |

### Courses

| Course | Lessons | Difficulty | Estimated Hours |
|--------|---------|------------|-----------------|
| Python Fundamentals | 20 | Beginner | 20 |
| Django Web Development | 25 | Intermediate | 30 |
| Data Structures & Algorithms | 25 | Intermediate | 35 |
| Machine Learning Basics | 25 | Advanced | 40 |

### Progress Distribution

**Alice (52.6% overall)**:
- Python: 90% complete (18/20 lessons)
- Django: 60% complete (15/25 lessons)
- DSA: 60% complete (15/25 lessons)
- ML: 16.7% complete (2/25 lessons)

**Bob (36.8% overall)**:
- Python: 75% complete (15/20 lessons)
- Django: 40% complete (10/25 lessons)
- DSA: 40% complete (10/25 lessons)
- ML: 0% complete (0/25 lessons)

**Charlie (11.6% overall)**:
- Python: 40% complete (8/20 lessons)
- Django: 8% complete (2/25 lessons)
- DSA: 4% complete (1/25 lessons)
- ML: 0% complete (0/25 lessons)

---

## 🎨 UI/UX Features

### Design Principles

- **Clean & Minimal**: Focus on content and data
- **Intuitive Navigation**: Easy access to all features
- **Responsive Design**: Works on all screen sizes
- **Accessible**: WCAG 2.1 compliant
- **Fast Loading**: Optimized performance

### Key Components

#### Dashboard Cards
- Summary statistics with icons
- Color-coded progress indicators
- Quick action buttons

#### Charts & Visualizations
- **Time Series Chart**: 30-day learning trend with smooth curves
- **Donut Chart**: Completion distribution with tooltips
- **Progress Bars**: Per-course completion with percentages

#### Course Cards
- Hover effects and shadows
- Badge indicators for difficulty
- Progress rings for visual feedback

#### Responsive Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

---

## 🔒 Security Features

### Authentication Security

- **JWT Tokens**: Secure, stateless authentication
- **Token Expiration**: Access tokens expire after 60 minutes
- **Password Hashing**: Bcrypt with strong salt rounds
- **HTTPS Ready**: SSL/TLS support for production

### API Security

- **CORS Configuration**: Whitelist allowed origins
- **Rate Limiting**: Prevent abuse (recommended for production)
- **SQL Injection Protection**: Django ORM parameterized queries
- **XSS Protection**: React's built-in sanitization

### Best Practices

- Environment variables for sensitive data
- No secrets in version control
- Regular dependency updates
- Input validation on all forms

---

## 📈 Performance Optimization

### Backend Optimization

- **Database Indexing**: Foreign keys and frequently queried fields
- **Query Optimization**: `select_related()` and `prefetch_related()`
- **Caching**: Redis for session and API response caching (optional)
- **Pagination**: Large result sets paginated

### Frontend Optimization

- **Code Splitting**: Lazy loading of routes
- **Image Optimization**: Compressed and appropriately sized
- **Bundle Size**: Tree shaking and minification
- **Memoization**: React.memo for expensive components

---

## 🔄 Adaptive Recommendation Algorithm

### Implementation Overview

Location: `backend/report/services/RecommendationService.py`

The recommendation engine analyzes student behavior and generates personalized suggestions using six distinct strategies. The algorithm executes in sequence and combines results based on priority scoring.

### Core Algorithm Flow

```python
def generate_recommendations(student, limit=5):
    """
    Main recommendation generation method
    Returns top 5 recommendations sorted by priority
    """
    recommendations = []
    
    # 1. Clear old recommendations
    Recommendation.objects.filter(student=student).delete()
    
    # 2. Execute all strategies
    recommendations.extend(recommend_in_progress(student))
    recommendations.extend(recommend_course_gaps(student))
    recommendations.extend(recommend_next_lessons(student))
    recommendations.extend(recommend_reviews(student))
    recommendations.extend(recommend_new_courses(student))
    
    # 3. Fallback for new students
    if len(recommendations) == 0:
        recommendations.extend(recommend_beginner_courses(student))
    
    # 4. Sort by priority and save top N
    recommendations.sort(key=lambda x: x['priority'], reverse=True)
    
    # 5. Save to database
    for rec in recommendations[:limit]:
        Recommendation.objects.create(
            student=student,
            lesson=rec['lesson'],
            reason=rec['reason'],
            priority=rec['priority']
        )
```

### Strategy 1: In-Progress Lessons (Priority: 70-90)

**Logic**: Prioritize lessons already started, with higher priority for recent activity.

```python
def recommend_in_progress(student):
    # Fetch lessons with status='in_progress'
    in_progress = Progress.objects.filter(
        student=student,
        status='in_progress'
    ).select_related('lesson', 'lesson__course').order_by('-last_accessed')[:3]
    
    for progress in in_progress:
        days_since_access = (timezone.now() - progress.last_accessed).days
        
        # Priority decreases with time: 90 → 85 → 80...
        priority = 90 - (days_since_access * 5)
        priority = max(priority, 70)  # Minimum priority: 70
        
        reason = f"You're {progress.time_spent_minutes} minutes into this lesson"
        if days_since_access > 3:
            reason += f" (last accessed {days_since_access} days ago)"
```

**Example Output**: *"You're 20 minutes into this lesson (last accessed 2 days ago)"*

### Strategy 2: Course Gaps (Priority: 60-88)

**Logic**: Recommend completing courses with 50-95% progress.

```python
def recommend_course_gaps(student):
    courses = Course.objects.filter(is_published=True).prefetch_related('lessons')
    
    for course in courses:
        total_lessons = course.lessons.count()
        completed_count = Progress.objects.filter(
            student=student,
            lesson__course=course,
            status='completed'
        ).count()
        
        progress_percentage = (completed_count / total_lessons) * 100
        
        # Only recommend if 50% ≤ progress < 95%
        if 50 <= progress_percentage < 95:
            # Find next incomplete lesson in order
            completed_lesson_ids = Progress.objects.filter(...).values_list('lesson_id', flat=True)
            next_lesson = course.lessons.exclude(id__in=completed_lesson_ids).order_by('order').first()
            
            # Priority: 60 + (progress% × 0.3) = 60 to 88.5
            priority = 60 + int(progress_percentage * 0.3)
            
            reason = f"You're {progress_percentage:.0f}% through {course.title} - finish strong!"
```

**Example Output**: *"You're 85% through Python Fundamentals - finish strong!"*

### Strategy 3: Next Sequential Lessons (Priority: 55)

**Logic**: Suggest next lesson in courses with recent activity (last 7 days).

```python
def recommend_next_lessons(student):
    # Get courses with activity in last 7 days
    recent_activity = Activity.objects.filter(
        student=student,
        timestamp__gte=timezone.now() - timedelta(days=7)
    ).values_list('lesson__course_id', flat=True).distinct()
    
    active_courses = Course.objects.filter(id__in=recent_activity, is_published=True)
    
    for course in active_courses:
        completed_lesson_ids = Progress.objects.filter(...).values_list('lesson_id', flat=True)
        
        # Find first incomplete lesson
        next_lesson = course.lessons.exclude(id__in=completed_lesson_ids).order_by('order').first()
        
        if next_lesson:
            # Verify previous lesson was completed
            prev_lessons = course.lessons.filter(order__lt=next_lesson.order).order_by('-order')
            
            if prev_lessons.exists():
                last_completed = Progress.objects.filter(
                    student=student,
                    lesson=prev_lessons.first(),
                    status='completed'
                ).exists()
                
                if last_completed:
                    priority = 55
                    reason = f"Next lesson in {course.title}"
```

**Example Output**: *"Next lesson in Django Web Development"*

### Strategy 4: Review Weak Lessons (Priority: 40)

**Logic**: Suggest reviewing completed lessons with time_spent < 50% of estimated time.

```python
def recommend_reviews(student):
    # Find lessons with low time investment
    weak_lessons = Progress.objects.filter(
        student=student,
        status='completed',
        lesson__estimated_minutes__gt=0
    ).select_related('lesson').annotate(
        time_ratio=F('time_spent_minutes') * 100.0 / F('lesson__estimated_minutes')
    ).filter(time_ratio__lt=50).order_by('time_ratio')[:2]
    
    for progress in weak_lessons:
        priority = 40
        reason = f"Quick review - you spent only {progress.time_spent_minutes}/{progress.lesson.estimated_minutes} min on this"
```

**Example Output**: *"Quick review - you spent only 10/30 min on this"*

### Strategy 5: New Course Suggestions (Priority: 30)

**Logic**: If student completed any course 100%, suggest new courses not yet started.

```python
def recommend_new_courses(student):
    courses = Course.objects.filter(is_published=True).prefetch_related('lessons')
    
    for course in courses:
        total_lessons = course.lessons.count()
        completed_count = Progress.objects.filter(
            student=student,
            lesson__course=course,
            status='completed'
        ).count()
        
        # Check if course is 100% complete
        if completed_count == total_lessons:
            # Find courses not started
            started_course_ids = Progress.objects.filter(student=student).values_list('lesson__course_id', flat=True).distinct()
            
            new_courses = Course.objects.filter(is_published=True).exclude(id__in=started_course_ids)[:2]
            
            for new_course in new_courses:
                first_lesson = new_course.lessons.order_by('order').first()
                if first_lesson:
                    priority = 30
                    reason = f"Start a new challenge: {new_course.title}"
            break
```

**Example Output**: *"Start a new challenge: Machine Learning Basics"*

### Strategy 6: Beginner Path (Priority: 85)

**Logic**: For new students with no progress, recommend beginner courses.

```python
def recommend_beginner_courses(student):
    # Get beginner-level courses
    beginner_courses = Course.objects.filter(
        is_published=True,
        difficulty='beginner'
    ).prefetch_related('lessons').order_by('id')[:3]
    
    for course in beginner_courses:
        first_lesson = course.lessons.order_by('order').first()
        if first_lesson:
            priority = 85
            reason = f"Start your learning journey with {course.title}"
    
    # Fallback: if no beginner courses, recommend any course
    if len(recommendations) == 0:
        all_courses = Course.objects.filter(is_published=True)[:3]
        for course in all_courses:
            first_lesson = course.lessons.order_by('order').first()
            if first_lesson:
                priority = 80
                reason = f"Begin with {course.title}"
```

**Example Output**: *"Start your learning journey with Python Fundamentals"*

### Priority Scoring System

| Strategy | Priority Range | Condition |
|----------|---------------|-----------|
| In-Progress | 70-90 | 90 - (days_since_access × 5), min 70 |
| Course Gaps | 60-88 | 60 + (progress_percentage × 0.3) |
| Next Lessons | 55 | Fixed priority |
| Review | 40 | Fixed priority |
| New Courses | 30 | Fixed priority |
| Beginner Path | 85 | For new students only |

### Database Storage

```python
class Recommendation(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    reason = models.TextField()  # Human-readable explanation
    priority = models.IntegerField()  # 0-100 score
    is_dismissed = models.BooleanField(default=False)  # User can dismiss
    created_at = models.DateTimeField(auto_now_add=True)
```

### API Integration

```python
# Dashboard endpoint automatically generates recommendations
def get_student_dashboard_data(student):
    # Check if recommendations exist
    existing_recs = Recommendation.objects.filter(
        student=student,
        is_dismissed=False
    ).count()
    
    # Generate if none exist
    if existing_recs == 0:
        RecommendationService.generate_recommendations(student)
    
    # Fetch active recommendations
    recs_result = RecommendationService.get_active_recommendations(student)
    
    return {
        'recommendations': recs_result['data']
    }
```

### Example API Response

```json
{
  "recommendations": [
    {
      "id": 1,
      "lesson": {
        "id": 2,
        "title": "Variables and Data Types",
        "course_title": "Python Fundamentals",
        "estimated_minutes": 45
      },
      "reason": "You're 20 minutes into this lesson (last accessed 2 days ago)",
      "priority": 88,
      "created_at": "2025-01-22T10:30:00Z"
    },
    {
      "id": 2,
      "lesson": {
        "id": 18,
        "title": "Control Flow - Loops",
        "course_title": "Python Fundamentals",
        "estimated_minutes": 60
      },
      "reason": "You're 85% through Python Fundamentals - finish strong!",
      "priority": 75,
      "created_at": "2025-01-22T10:30:00Z"
    }
  ]
}
```

---

## 📱 Mobile Responsiveness

### Mobile-First Design

The application is fully responsive with optimized layouts for:

#### Mobile (< 640px)
- Single column layout
- Collapsible navigation menu
- Touch-friendly buttons (min 44x44px)
- Simplified charts for small screens
- Bottom navigation bar

#### Tablet (640px - 1024px)
- Two-column grid for courses
- Side navigation drawer
- Larger touch targets
- Full-featured charts

#### Desktop (> 1024px)
- Multi-column layouts
- Persistent sidebar navigation
- Hover interactions
- Full-featured dashboard with all widgets

---

## 🌐 Internationalization (Future)

### Planned i18n Support

- Multi-language support (English, Spanish, French, German)
- RTL language support (Arabic, Hebrew)
- Localized date/time formats
- Currency localization
- Timezone handling

---

## 🔮 Future Enhancements

### Planned Features

#### Phase 1: Enhanced Analytics
- [ ] Weekly/monthly reports via email
- [ ] Export progress to PDF
- [ ] Advanced filtering and search
- [ ] Custom date range selection

#### Phase 2: Social Features
- [ ] Student discussion forums
- [ ] Peer-to-peer study groups
- [ ] Achievement badges and gamification
- [ ] Leaderboards

#### Phase 3: Content Management
- [ ] Course creation interface for mentors
- [ ] Rich text editor for lessons
- [ ] Video upload and streaming
- [ ] Quiz builder with auto-grading

#### Phase 4: Advanced Features
- [ ] Mobile apps (iOS/Android)
- [ ] Offline mode with sync
- [ ] AI-powered chatbot assistant
- [ ] Integration with Google Classroom, Canvas

#### Phase 5: Enterprise Features
- [ ] Organization management
- [ ] Team dashboards
- [ ] Custom branding
- [ ] SSO integration
- [ ] Advanced reporting and analytics

---

## 📞 Support & Contact

### Getting Help

- **Documentation**: Refer to this README and API docs
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Email**: support@learningtracker.com (if available)

### Reporting Bugs

When reporting bugs, please include:
- Operating system and version
- Browser and version (for frontend issues)
- Python version (for backend issues)
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Error messages and logs

### Feature Requests

We welcome feature requests! Please:
- Check existing issues first
- Describe the use case
- Explain expected behavior
- Provide mockups if possible

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

---

## 🙏 Acknowledgments

### Technologies Used

- [Django](https://www.djangoproject.com/) - High-level Python web framework
- [Django REST Framework](https://www.django-rest-framework.org/) - Powerful toolkit for building Web APIs
- [React](https://reactjs.org/) - JavaScript library for building user interfaces
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [Recharts](https://recharts.org/) - Composable charting library
- [PostgreSQL](https://www.postgresql.org/) - Advanced open source database
- [Vite](https://vitejs.dev/) - Next generation frontend tooling

### Inspiration

This project was built as part of a full-stack development challenge to demonstrate:
- Modern web application architecture
- RESTful API design
- User authentication and authorization
- Data visualization and analytics
- Adaptive algorithms and intelligent systems

---

## 📚 Additional Resources

### Learning Materials

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [REST API Best Practices](https://restfulapi.net/)

### Related Projects

- [Learning Management Systems](https://github.com/topics/lms)
- [Progress Tracking Apps](https://github.com/topics/progress-tracker)
- [Educational Platforms](https://github.com/topics/education)

---

## 🎯 Project Goals

This project demonstrates proficiency in:

✅ **Full-Stack Development**
- Backend API development with Django
- Frontend SPA development with React
- Database design and optimization

✅ **Software Engineering**
- Clean code architecture
- Service-layer pattern
- Separation of concerns
- RESTful API design

✅ **User Experience**
- Responsive design
- Intuitive navigation
- Data visualization
- Accessibility

✅ **Advanced Features**
- JWT authentication
- Role-based access control
- Adaptive algorithms
- Real-time data updates

✅ **DevOps & Deployment**
- Environment configuration
- Database migrations
- Static file handling
- Production readiness

---

## 📊 Project Statistics

- **Total Lines of Code**: ~8,000+
- **Backend Files**: 40+
- **Frontend Components**: 25+
- **API Endpoints**: 15+
- **Database Tables**: 6
- **Test Coverage**: 70%+ (goal)

---

## 🎓 Learning Outcomes

By exploring this project, you'll learn:

1. **Backend Development**
   - Django project structure
   - RESTful API design
   - Database modeling with Django ORM
   - Service layer architecture
   - JWT authentication

2. **Frontend Development**
   - React hooks and context
   - API integration with Axios
   - Chart libraries (Recharts)
   - Tailwind CSS styling
   - Responsive design

3. **System Design**
   - User authentication flow
   - Role-based access control
   - Progress tracking systems
   - Recommendation algorithms
   - Analytics dashboards

4. **Best Practices**
   - Environment configuration
   - Error handling
   - Code organization
   - Documentation
   - Version control

---

## 🚀 Quick Start Summary

```bash
# Backend
cd backend
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm install
npm run dev

# Access at http://localhost:5173
# Login: alice@test.com / password123
```

---

## ✨ Contributors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

See also the list of [contributors](https://github.com/yourusername/learning-tracker/contributors) who participated in this project.

---

## 📝 Changelog

### Version 1.0.0 (2025-01-22)
- ✅ Initial release
- ✅ JWT authentication
- ✅ Student and mentor dashboards
- ✅ Progress tracking
- ✅ Adaptive recommendations
- ✅ Time series analytics
- ✅ Responsive UI



<div align="center">

**Made with ❤️ by Nimanita**

⭐ **Star this repo if you find it useful!** ⭐


</div>

---

*Last Updated: January 2025*