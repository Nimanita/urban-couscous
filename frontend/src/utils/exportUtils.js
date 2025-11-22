// src/utils/exportUtils.js
import Papa from 'papaparse';

/**
 * Export dashboard data to CSV
 */
export const exportDashboardToCSV = (dashboardData, userName) => {
  const timestamp = new Date().toISOString().split('T')[0];
  const filename = `${userName}_dashboard_${timestamp}.csv`;

  const { summary, course_progress, time_series } = dashboardData;

  // Create summary data
  const summaryData = [
    ['Dashboard Summary'],
    ['Total Lessons Completed', summary.total_lessons_completed],
    ['Total Time (minutes)', summary.total_time_minutes],
    ['Courses In Progress', summary.courses_in_progress],
    ['Overall Progress (%)', summary.overall_progress_percentage.toFixed(2)],
    ['Learning Streak (days)', dashboardData.learning_streak || 0],
    [],
  ];

  // Course progress data
  const courseData = [
    ['Course Progress'],
    ['Course Name', 'Progress (%)'],
    ...course_progress.map(c => [c.course_name, c.progress]),
    [],
  ];

  // Time series data (last 7 days)
  const recentTimeSeries = time_series.slice(-7);
  const timeSeriesData = [
    ['Recent Activity (Last 7 Days)'],
    ['Date', 'Minutes'],
    ...recentTimeSeries.map(t => [t.date, t.minutes]),
  ];

  // Combine all data
  const allData = [...summaryData, ...courseData, ...timeSeriesData];

  // Convert to CSV
  const csv = Papa.unparse(allData);

  // Download
  downloadCSV(csv, filename);
};

/**
 * Export course details with lessons to CSV
 */
export const exportCourseToCSV = (course, lessons, userName) => {
  const timestamp = new Date().toISOString().split('T')[0];
  const filename = `${course.title.replace(/\s+/g, '_')}_${timestamp}.csv`;

  // Course info
  const courseInfo = [
    ['Course Information'],
    ['Course Name', course.title],
    ['Description', course.description],
    ['Difficulty', course.difficulty],
    ['Category', course.category],
    ['Estimated Hours', course.estimated_hours],
    [],
  ];

  // Calculate progress
  const completedLessons = lessons.filter(l => l.status === 'completed').length;
  const totalLessons = lessons.length;
  const progressPercentage = totalLessons > 0 ? ((completedLessons / totalLessons) * 100).toFixed(2) : 0;

  const progressInfo = [
    ['Your Progress'],
    ['Total Lessons', totalLessons],
    ['Completed Lessons', completedLessons],
    ['Progress (%)', progressPercentage],
    [],
  ];

  // Lessons data
  const lessonsData = [
    ['Lessons'],
    ['#', 'Title', 'Status', 'Time Spent (min)', 'Estimated Time (min)', 'Content Type', 'Completed At', 'Notes'],
    ...lessons.map((lesson, index) => [
      index + 1,
      lesson.title,
      lesson.status || 'not_started',
      lesson.time_spent_minutes || 0,
      lesson.estimated_minutes,
      lesson.content_type,
      lesson.completed_at || '',
      lesson.notes || ''
    ]),
  ];

  // Combine all data
  const allData = [...courseInfo, ...progressInfo, ...lessonsData];

  // Convert to CSV
  const csv = Papa.unparse(allData);

  // Download
  downloadCSV(csv, filename);
};

/**
 * Export all courses list to CSV
 */
export const exportCoursesListToCSV = (courses, userName) => {
  const timestamp = new Date().toISOString().split('T')[0];
  const filename = `${userName}_courses_${timestamp}.csv`;

  const data = [
    ['Course Name', 'Difficulty', 'Category', 'Estimated Hours', 'Total Lessons', 'Completed Lessons', 'Progress (%)', 'Time Spent (min)', 'Status'],
    ...courses.map(course => [
      course.title,
      course.difficulty,
      course.category,
      course.estimated_hours,
      course.total_lessons || 0,
      course.completed_lessons || 0,
      course.progress_percentage || 0,
      course.time_spent_minutes || 0,
      course.status || 'not_started'
    ])
  ];

  const csv = Papa.unparse(data);
  downloadCSV(csv, filename);
};

/**
 * Export recommendations to CSV
 */
export const exportRecommendationsToCSV = (recommendations, userName) => {
  const timestamp = new Date().toISOString().split('T')[0];
  const filename = `${userName}_recommendations_${timestamp}.csv`;

  const data = [
    ['Course', 'Lesson', 'Reason', 'Priority', 'Estimated Time (min)', 'Created At'],
    ...recommendations.map(rec => [
      rec.lesson.course_title,
      rec.lesson.title,
      rec.reason,
      rec.priority,
      rec.lesson.estimated_minutes,
      new Date(rec.created_at).toLocaleDateString()
    ])
  ];

  const csv = Papa.unparse(data);
  downloadCSV(csv, filename);
};

/**
 * Helper function to trigger CSV download
 */
const downloadCSV = (csv, filename) => {
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
};