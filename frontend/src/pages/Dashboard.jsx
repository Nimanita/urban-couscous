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
import { BookOpen, Clock, TrendingUp, Award, Flame, Lightbulb } from 'lucide-react';
import { formatTime } from '../utils/helpers';

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
      // Refresh dashboard to update recommendations
      fetchDashboard();
    } catch (error) {
      console.error('Failed to dismiss recommendation:', error);
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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">
              Welcome back, {user?.first_name}!
            </h1>
            <p className="text-gray-600 mt-1">
              Track your learning progress and achievements
            </p>
          </div>

          {/* Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <MetricCard
              title="Lessons Completed"
              value={summary.total_lessons_completed}
              icon={BookOpen}
              color="blue"
            />
            <MetricCard
              title="Time Spent Learning"
              value={formatTime(summary.total_time_minutes)}
              icon={Clock}
              color="green"
            />
            <MetricCard
              title="Courses In Progress"
              value={summary.courses_in_progress}
              icon={TrendingUp}
              color="purple"
            />
            <MetricCard
              title="Overall Progress"
              value={`${summary.overall_progress_percentage.toFixed(1)}%`}
              icon={Award}
              color="orange"
              subtitle={learning_streak > 0 ? `🔥 ${learning_streak} day streak!` : ''}
            />
          </div>

          {/* Learning Streak Badge */}
          {learning_streak >= 7 && (
            <div className="mb-8 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-xl p-6 shadow-lg">
              <div className="flex items-center gap-4">
                <div className="bg-white bg-opacity-20 p-4 rounded-full">
                  <Flame className="h-8 w-8" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold">{learning_streak} Day Streak! 🎉</h3>
                  <p className="text-orange-100">Keep up the amazing work!</p>
                </div>
              </div>
            </div>
          )}

          {/* Charts and Recommendations Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <div className="lg:col-span-2">
              <TimeSeriesChart data={time_series} />
            </div>
            
            {/* Recommendations Section */}
            {recommendations.length > 0 && (
              <div className="card">
                <div className="flex items-center gap-2 mb-4">
                  <Lightbulb className="h-5 w-5 text-yellow-500" />
                  <h3 className="text-lg font-semibold text-gray-900">Recommended</h3>
                </div>
                <div className="space-y-3">
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
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <ProgressBarChart data={course_progress} />
            <DonutChart data={completion_distribution} />
          </div>

          {/* Quick Stats */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                <span className="text-sm font-medium text-gray-700">Avg. Session Time</span>
                <span className="text-lg font-bold text-primary-600">
                  {formatTime(Math.round(summary.total_time_minutes / Math.max(summary.total_lessons_completed, 1)))}
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                <span className="text-sm font-medium text-gray-700">Completion Rate</span>
                <span className="text-lg font-bold text-green-600">
                  {summary.overall_progress_percentage.toFixed(1)}%
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-purple-50 rounded-lg">
                <span className="text-sm font-medium text-gray-700">Active Courses</span>
                <span className="text-lg font-bold text-purple-600">
                  {summary.courses_in_progress}
                </span>
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
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Mentor Dashboard</h1>
          <p className="text-gray-600 mt-1">Monitor student progress and provide guidance</p>
        </div>

        {/* Mentor Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <MetricCard
            title="Total Students"
            value={total_students}
            icon={BookOpen}
            color="blue"
          />
          <MetricCard
            title="Average Completion"
            value={`${average_completion_rate.toFixed(1)}%`}
            icon={TrendingUp}
            color="green"
          />
          <MetricCard
            title="Students Needing Help"
            value={students_needing_help.length}
            icon={Award}
            color="orange"
          />
        </div>

        {/* Students Needing Help */}
        {students_needing_help.length > 0 && (
          <div className="card mb-8 bg-orange-50 border-orange-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              ⚠️ Students Needing Attention
            </h3>
            <div className="space-y-3">
              {students_needing_help.map((student) => (
                <div key={student.student_id} className="bg-white p-4 rounded-lg">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-medium text-gray-900">{student.student_name}</p>
                      <p className="text-sm text-gray-600">{student.student_email}</p>
                    </div>
                    <span className="text-orange-600 font-bold">
                      {student.stats.overall_progress_percentage.toFixed(1)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* All Students */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">All Students</h3>
          <div className="space-y-4">
            {students.map((student) => (
              <div key={student.student_id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <p className="font-semibold text-gray-900">{student.student_name}</p>
                    <p className="text-sm text-gray-600">{student.student_email}</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">Lessons Completed</p>
                    <p className="font-bold text-primary-600">{student.stats.total_lessons_completed}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Time Spent</p>
                    <p className="font-bold text-green-600">{formatTime(student.stats.total_time_minutes)}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Active Courses</p>
                    <p className="font-bold text-purple-600">{student.stats.courses_in_progress}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Progress</p>
                    <p className="font-bold text-orange-600">{student.stats.overall_progress_percentage.toFixed(1)}%</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
};

export default Dashboard;