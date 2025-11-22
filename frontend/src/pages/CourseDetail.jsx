// src/pages/CourseDetail.jsx
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { coursesAPI } from '../api/courses';
import Navbar from '../components/common/Navbar';
import LoadingSpinner from '../components/common/LoadingSpinner';
import LessonList from '../components/courses/LessonList';
import { ArrowLeft, BookOpen, Clock, TrendingUp } from 'lucide-react';
import { getDifficultyColor, formatTime } from '../utils/helpers';
import { useAuth } from '../context/AuthContext';

const CourseDetail = () => {
  const { id } = useParams();
  const { isStudent } = useAuth();
  const [course, setCourse] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourseDetails();
  }, [id]);

  const fetchCourseDetails = async () => {
    try {
      const [courseResponse, lessonsResponse] = await Promise.all([
        coursesAPI.getCourseById(id),
        coursesAPI.getCourseLessons(id),
      ]);
      setCourse(courseResponse.data);
      setLessons(lessonsResponse.data);
    } catch (error) {
      console.error('Failed to fetch course details:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <>
        <Navbar />
        <LoadingSpinner fullScreen />
      </>
    );
  }

  if (!course) {
    return (
      <>
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="card text-center">
            <p className="text-gray-600">Course not found.</p>
            <Link to="/courses" className="btn-primary mt-4 inline-block">
              Back to Courses
            </Link>
          </div>
        </div>
      </>
    );
  }

  // Calculate progress statistics for students
  const completedLessons = isStudent
    ? lessons.filter((l) => l.status === 'completed').length
    : 0;
  const totalLessons = lessons.length;
  const progressPercentage = totalLessons > 0
    ? Math.round((completedLessons / totalLessons) * 100)
    : 0;
  const totalTimeSpent = isStudent
    ? lessons.reduce((sum, l) => sum + (l.time_spent_minutes || 0), 0)
    : 0;

  return (
    <>
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back Button */}
        <Link
          to="/courses"
          className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-6"
        >
          <ArrowLeft className="h-4 w-4 mr-1" />
          Back to Courses
        </Link>

        {/* Course Header */}
        <div className="card mb-8">
          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-3">
                <h1 className="text-3xl font-bold text-gray-900">
                  {course.title}
                </h1>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(
                    course.difficulty
                  )}`}
                >
                  {course.difficulty}
                </span>
              </div>
              <p className="text-gray-600 mb-4">{course.description}</p>

              <div className="flex flex-wrap gap-4 text-sm text-gray-500">
                <div className="flex items-center gap-1">
                  <BookOpen className="h-4 w-4" />
                  <span>{totalLessons} lessons</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="h-4 w-4" />
                  <span>~{course.estimated_hours} hours</span>
                </div>
                <div className="flex items-center gap-1">
                  <span className="capitalize">
                    Category: {course.category.replace('_', ' ')}
                  </span>
                </div>
              </div>
            </div>

            {isStudent && (
              <div className="bg-primary-50 p-6 rounded-lg min-w-[240px]">
                <div className="text-center">
                  <div className="text-4xl font-bold text-primary-600 mb-2">
                    {progressPercentage}%
                  </div>
                  <p className="text-sm text-gray-600 mb-4">Course Progress</p>
                  <div className="space-y-2 text-left">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Completed:</span>
                      <span className="font-semibold">
                        {completedLessons}/{totalLessons}
                      </span>
                    </div>
                    {totalTimeSpent > 0 && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Time Spent:</span>
                        <span className="font-semibold">
                          {formatTime(totalTimeSpent)}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>

          {isStudent && (
            <div className="mt-6">
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-primary-600 h-3 rounded-full transition-all"
                  style={{ width: `${progressPercentage}%` }}
                />
              </div>
            </div>
          )}
        </div>

        {/* Lessons Section */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Course Lessons</h2>
            <div className="text-sm text-gray-600">
              {totalLessons} lesson{totalLessons !== 1 ? 's' : ''}
            </div>
          </div>

          {lessons.length === 0 ? (
            <div className="card text-center py-12">
              <p className="text-gray-600">No lessons available yet.</p>
            </div>
          ) : (
            <LessonList
              lessons={lessons}
              onProgressUpdate={fetchCourseDetails}
            />
          )}
        </div>
      </div>
    </>
  );
};

export default CourseDetail;