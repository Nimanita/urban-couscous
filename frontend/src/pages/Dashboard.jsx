// src/pages/Dashboard.jsx
import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { dashboardAPI } from '../api/dashboard';
import Navbar from '../components/common/Navbar';
import AdminNavbar from '../components/common/AdminNavbar';
import LoadingSpinner from '../components/common/LoadingSpinner';
import MetricCard from '../components/common/MetricCard';
import TimeSeriesChart from '../components/dashboard/TimeSeriesChart';
import ProgressBarChart from '../components/dashboard/ProgressBarChart';
import DonutChart from '../components/dashboard/DonutChart';
import RecommendationCard from '../components/dashboard/RecommendationCard';
import { BookOpen, Clock, TrendingUp, Award, Flame, Lightbulb, Download } from 'lucide-react';
import { formatTime } from '../utils/helpers';
import { exportDashboardToCSV, exportRecommendationsToCSV } from '../utils/exportUtils';

const Dashboard = () => {
  const { user, isStudent } = useAuth();
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await dashboardAPI.getDashboard();
      setDashboardData(response.data);
    } catch (error) {
      console.error('Failed to fetch dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDismissRecommendation = async (recId) => {
    try {
      await dashboardAPI.dismissRecommendation(recId);
      fetchDashboard();
    } catch (error) {
      console.error('Failed to dismiss recommendation:', error);
    }
  };

  const handleExportDashboard = () => {
    if (dashboardData) {
      exportDashboardToCSV(dashboardData, user.first_name);
    }
  };

  const handleExportRecommendations = () => {
    if (dashboardData && dashboardData.recommendations) {
      exportRecommendationsToCSV(dashboardData.recommendations, user.first_name);
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

  if (isStudent) {
    const { 
      summary, 
      time_series, 
      course_progress, 
      completion_distribution, 
      learning_streak,
      recommendations = []
    } = dashboardData;

    return (
      <>
        <Navbar />
        <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Header Section */}
            <div className="mb-8">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                  <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                    Welcome back, {user?.first_name}!
                  </h1>
                  <p className="text-gray-600 mt-2 text-lg">
                    Track your learning progress and achievements
                  </p>
                </div>
                <button
                  onClick={handleExportDashboard}
                  className="btn-primary flex items-center gap-2 shadow-lg hover:shadow-xl transition-shadow"
                >
                  <Download className="h-4 w-4" />
                  Export CSV
                </button>
              </div>
            </div>

            {/* Metrics Grid with Enhanced Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all p-6 border-l-4 border-blue-500">
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 bg-blue-100 rounded-xl">
                    <BookOpen className="h-6 w-6 text-blue-600" />
                  </div>
                  <span className="text-3xl font-bold text-gray-900">{summary.total_lessons_completed}</span>
                </div>
                <p className="text-gray-600 font-medium">Lessons Completed</p>
              </div>

              <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all p-6 border-l-4 border-green-500">
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 bg-green-100 rounded-xl">
                    <Clock className="h-6 w-6 text-green-600" />
                  </div>
                  <span className="text-3xl font-bold text-gray-900">{formatTime(summary.total_time_minutes)}</span>
                </div>
                <p className="text-gray-600 font-medium">Time Spent Learning</p>
              </div>

              <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all p-6 border-l-4 border-purple-500">
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 bg-purple-100 rounded-xl">
                    <TrendingUp className="h-6 w-6 text-purple-600" />
                  </div>
                  <span className="text-3xl font-bold text-gray-900">{summary.courses_in_progress}</span>
                </div>
                <p className="text-gray-600 font-medium">Courses In Progress</p>
              </div>

              <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all p-6 border-l-4 border-orange-500">
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 bg-orange-100 rounded-xl">
                    <Award className="h-6 w-6 text-orange-600" />
                  </div>
                  <span className="text-3xl font-bold text-gray-900">{summary.overall_progress_percentage.toFixed(1)}%</span>
                </div>
                <p className="text-gray-600 font-medium">Overall Progress</p>
                {learning_streak > 0 && (
                  <div className="mt-3 flex items-center gap-2 text-orange-600">
                    <Flame className="h-4 w-4" />
                    <span className="text-sm font-semibold">{learning_streak} day streak!</span>
                  </div>
                )}
              </div>
            </div>

            {/* Learning Streak Badge */}
            {learning_streak >= 7 && (
              <div className="mb-8 bg-gradient-to-r from-orange-500 via-red-500 to-pink-500 text-white rounded-2xl p-6 shadow-2xl">
                <div className="flex items-center gap-4">
                  <div className="bg-white bg-opacity-20 p-4 rounded-2xl backdrop-blur-sm">
                    <Flame className="h-10 w-10" />
                  </div>
                  <div>
                    <h3 className="text-3xl font-bold">{learning_streak} Day Streak! 🎉</h3>
                    <p className="text-orange-100 text-lg mt-1">You're on fire! Keep up the amazing work!</p>
                  </div>
                </div>
              </div>
            )}

            {/* Main Content Grid - Modern Layout */}
            <div className="grid grid-cols-1 xl:grid-cols-12 gap-6 mb-8">
              {/* Left Column - Charts (8 columns) */}
              <div className="xl:col-span-8 space-y-6">
                {/* Time Series Chart - Full Width */}
                <div className="bg-white rounded-2xl shadow-lg p-6">
                  <TimeSeriesChart data={time_series} />
                </div>

                {/* Progress Charts - Side by Side */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="bg-white rounded-2xl shadow-lg p-6">
                    <ProgressBarChart data={course_progress} />
                  </div>
                  <div className="bg-white rounded-2xl shadow-lg p-6">
                    <DonutChart data={completion_distribution} />
                  </div>
                </div>
              </div>

              {/* Right Column - Recommendations & Quick Stats (4 columns) */}
              <div className="xl:col-span-4 space-y-6">
                {/* Recommendations */}
                {recommendations.length > 0 && (
                  <div className="bg-white rounded-2xl shadow-lg p-6">
                    <div className="flex items-center gap-3 mb-6">
                      <div className="p-2 bg-yellow-100 rounded-xl">
                        <Lightbulb className="h-5 w-5 text-yellow-600" />
                      </div>
                      <h3 className="text-xl font-bold text-gray-900">Recommended for You</h3>
                    </div>
                    <div className="space-y-4">
                      {recommendations.slice(0, 3).map((rec) => (
                        <RecommendationCard
                          key={rec.id}
                          recommendation={rec}
                          onDismiss={handleDismissRecommendation}
                        />
                      ))}
                    </div>
                  </div>
                )}

                {/* Quick Stats Card */}
                <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl shadow-lg p-6 text-white">
                  <h3 className="text-xl font-bold mb-6">Quick Stats</h3>
                  <div className="space-y-4">
                    <div className="bg-white bg-opacity-20 backdrop-blur-sm rounded-xl p-4">
                      <p className="text-sm opacity-90 mb-1">Avg. Session Time</p>
                      <p className="text-2xl font-bold">
                        {formatTime(Math.round(summary.total_time_minutes / Math.max(summary.total_lessons_completed, 1)))}
                      </p>
                    </div>
                    <div className="bg-white bg-opacity-20 backdrop-blur-sm rounded-xl p-4">
                      <p className="text-sm opacity-90 mb-1">Completion Rate</p>
                      <p className="text-2xl font-bold">{summary.overall_progress_percentage.toFixed(1)}%</p>
                    </div>
                    <div className="bg-white bg-opacity-20 backdrop-blur-sm rounded-xl p-4">
                      <p className="text-sm opacity-90 mb-1">Active Courses</p>
                      <p className="text-2xl font-bold">{summary.courses_in_progress}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </>
    );
  }

  // Mentor Dashboard
  const { total_students, average_completion_rate, students, students_needing_help } = dashboardData;

  return (
    <>
      <AdminNavbar />
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-8">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Mentor Dashboard
            </h1>
            <p className="text-gray-600 mt-2 text-lg">Monitor student progress and provide guidance</p>
          </div>

          {/* Mentor Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all p-6 border-l-4 border-blue-500">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-blue-100 rounded-xl">
                  <BookOpen className="h-6 w-6 text-blue-600" />
                </div>
                <span className="text-3xl font-bold text-gray-900">{total_students}</span>
              </div>
              <p className="text-gray-600 font-medium">Total Students</p>
            </div>

            <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all p-6 border-l-4 border-green-500">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-green-100 rounded-xl">
                  <TrendingUp className="h-6 w-6 text-green-600" />
                </div>
                <span className="text-3xl font-bold text-gray-900">{average_completion_rate.toFixed(1)}%</span>
              </div>
              <p className="text-gray-600 font-medium">Average Completion</p>
            </div>

            <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all p-6 border-l-4 border-orange-500">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-orange-100 rounded-xl">
                  <Award className="h-6 w-6 text-orange-600" />
                </div>
                <span className="text-3xl font-bold text-gray-900">{students_needing_help.length}</span>
              </div>
              <p className="text-gray-600 font-medium">Students Needing Help</p>
            </div>
          </div>

          {/* Students Needing Help */}
          {students_needing_help.length > 0 && (
            <div className="bg-white rounded-2xl shadow-lg p-6 mb-8 border-l-4 border-orange-500">
              <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                ⚠️ Students Needing Attention
              </h3>
              <div className="space-y-4">
                {students_needing_help.map((student) => (
                  <div key={student.student_id} className="bg-orange-50 p-4 rounded-xl border border-orange-200">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-semibold text-gray-900">{student.student_name}</p>
                        <p className="text-sm text-gray-600">{student.student_email}</p>
                      </div>
                      <span className="text-orange-600 font-bold text-xl">
                        {student.stats.overall_progress_percentage.toFixed(1)}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* All Students */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-6">All Students</h3>
            <div className="space-y-4">
              {students.map((student) => (
                <div key={student.student_id} className="border-2 border-gray-100 rounded-xl p-5 hover:border-blue-300 hover:shadow-md transition-all">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <p className="font-bold text-gray-900 text-lg">{student.student_name}</p>
                      <p className="text-sm text-gray-600">{student.student_email}</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-blue-50 rounded-lg p-3">
                      <p className="text-xs text-gray-600 mb-1">Lessons Completed</p>
                      <p className="text-xl font-bold text-blue-600">{student.stats.total_lessons_completed}</p>
                    </div>
                    <div className="bg-green-50 rounded-lg p-3">
                      <p className="text-xs text-gray-600 mb-1">Time Spent</p>
                      <p className="text-xl font-bold text-green-600">{formatTime(student.stats.total_time_minutes)}</p>
                    </div>
                    <div className="bg-purple-50 rounded-lg p-3">
                      <p className="text-xs text-gray-600 mb-1">Active Courses</p>
                      <p className="text-xl font-bold text-purple-600">{student.stats.courses_in_progress}</p>
                    </div>
                    <div className="bg-orange-50 rounded-lg p-3">
                      <p className="text-xs text-gray-600 mb-1">Progress</p>
                      <p className="text-xl font-bold text-orange-600">{student.stats.overall_progress_percentage.toFixed(1)}%</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Dashboard;