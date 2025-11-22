// src/components/dashboard/RecommendationCard.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Clock, X, BookOpen } from 'lucide-react';

const RecommendationCard = ({ recommendation, onDismiss }) => {
  const navigate = useNavigate();
  const [isDismissing, setIsDismissing] = useState(false);

  const getPriorityStyle = (priority) => {
    if (priority >= 80) {
      return {
        dot: 'bg-red-500',
        text: 'text-red-700',
        bg: 'bg-red-50'
      };
    } else if (priority >= 60) {
      return {
        dot: 'bg-orange-500',
        text: 'text-orange-700',
        bg: 'bg-orange-50'
      };
    } else if (priority >= 40) {
      return {
        dot: 'bg-blue-500',
        text: 'text-blue-700',
        bg: 'bg-blue-50'
      };
    } else {
      return {
        dot: 'bg-gray-500',
        text: 'text-gray-700',
        bg: 'bg-gray-50'
      };
    }
  };

  const handleDismiss = async (e) => {
    e.stopPropagation();
    setIsDismissing(true);
    await onDismiss(recommendation.id);
  };

  const handleClick = () => {
    navigate(`/courses`);
  };

  const styles = getPriorityStyle(recommendation.priority);

  return (
    <div
      className={`p-4 border border-gray-200 rounded-lg hover:shadow-md hover:border-primary-300 transition-all cursor-pointer relative ${
        isDismissing ? 'opacity-50' : ''
      }`}
      onClick={handleClick}
    >
      {/* Dismiss button */}
      <button
        onClick={handleDismiss}
        className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 transition-colors"
        title="Dismiss"
      >
        <X className="h-4 w-4" />
      </button>

      {/* Priority dot and course */}
      <div className="flex items-center gap-2 mb-2 pr-6">
        <div className={`w-2 h-2 rounded-full ${styles.dot}`} />
        <span className="text-xs text-gray-500 font-medium truncate">
          {recommendation.lesson.course_title}
        </span>
      </div>

      {/* Lesson title */}
      <h4 className="font-semibold text-gray-900 text-sm mb-2 line-clamp-2 pr-4">
        {recommendation.lesson.title}
      </h4>

      {/* Reason */}
      <p className={`text-xs ${styles.text} mb-3 line-clamp-2`}>
        {recommendation.reason}
      </p>

      {/* Footer */}
      <div className="flex items-center justify-between text-xs text-gray-500">
        <div className="flex items-center gap-1">
          <Clock className="h-3 w-3" />
          <span>{recommendation.lesson.estimated_minutes} min</span>
        </div>
        <div className="flex items-center gap-1">
          <BookOpen className="h-3 w-3" />
          <span className="text-primary-600 font-medium">View</span>
        </div>
      </div>
    </div>
  );
};

export default RecommendationCard;