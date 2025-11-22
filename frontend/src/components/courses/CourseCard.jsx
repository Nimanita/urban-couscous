// src/components/courses/CourseCard.jsx
import { Link } from 'react-router-dom';
import { BookOpen, Clock, TrendingUp } from 'lucide-react';
import { getDifficultyColor, formatTime } from '../../utils/helpers';

const CourseCard = ({ course }) => {
  const isStudent = course.hasOwnProperty('progress_percentage');

  return (
    <Link
      to={`/courses/${course.id}`}
      className="card hover:shadow-lg transition-all hover:scale-[1.02] cursor-pointer"
    >
      <div className="flex items-start justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
          {course.title}
        </h3>
        <span
          className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(
            course.difficulty
          )}`}
        >
          {course.difficulty}
        </span>
      </div>

      <p className="text-sm text-gray-600 mb-4 line-clamp-3">
        {course.description}
      </p>

      <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
        <div className="flex items-center gap-1">
          <BookOpen className="h-4 w-4" />
          <span>{isStudent ? course.total_lessons : '...'} lessons</span>
        </div>
        <div className="flex items-center gap-1">
          <Clock className="h-4 w-4" />
          <span>{course.estimated_hours}h</span>
        </div>
      </div>

      {isStudent && (
        <>
          <div className="mb-2">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600">Progress</span>
              <span className="font-medium text-primary-600">
                {course.progress_percentage}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-primary-600 h-2 rounded-full transition-all"
                style={{ width: `${course.progress_percentage}%` }}
              />
            </div>
          </div>

          {course.time_spent_minutes > 0 && (
            <div className="flex items-center gap-1 text-sm text-gray-500 mt-2">
              <TrendingUp className="h-4 w-4" />
              <span>{formatTime(course.time_spent_minutes)} spent</span>
            </div>
          )}
        </>
      )}
    </Link>
  );
};

export default CourseCard;