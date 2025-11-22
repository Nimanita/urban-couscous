// src/components/courses/LessonList.jsx
import { CheckCircle2, Circle, Clock, PlayCircle } from 'lucide-react';
import { formatTime, getStatusColor, formatStatus } from '../../utils/helpers';
import { useState } from 'react';
import { progressAPI } from '../../api/progress';

const LessonList = ({ lessons, onProgressUpdate }) => {
  const [updatingLesson, setUpdatingLesson] = useState(null);

  const handleMarkComplete = async (lessonId) => {
    setUpdatingLesson(lessonId);
    try {
      await progressAPI.markLessonComplete(lessonId, 0);
      if (onProgressUpdate) onProgressUpdate();
    } catch (error) {
      console.error('Failed to mark lesson complete:', error);
      alert('Failed to update lesson status');
    } finally {
      setUpdatingLesson(null);
    }
  };

  return (
    <div className="space-y-3">
      {lessons.map((lesson) => {
        const hasProgress = lesson.progress;
        const status = hasProgress?.status || 'not_started';

        return (
          <div
            key={lesson.id}
            className="card hover:shadow-md transition-shadow"
          >
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 mt-1">
                {status === 'completed' ? (
                  <CheckCircle2 className="h-6 w-6 text-green-500" />
                ) : status === 'in_progress' ? (
                  <PlayCircle className="h-6 w-6 text-blue-500" />
                ) : (
                  <Circle className="h-6 w-6 text-gray-300" />
                )}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h4 className="text-base font-semibold text-gray-900">
                      {lesson.title}
                    </h4>
                    <p className="text-sm text-gray-600 mt-1">
                      {lesson.description}
                    </p>
                  </div>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium whitespace-nowrap ${getStatusColor(
                      status
                    )}`}
                  >
                    {formatStatus(status)}
                  </span>
                </div>

                <div className="flex flex-wrap items-center gap-4 mt-3 text-sm text-gray-500">
                  <div className="flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    <span>~{lesson.estimated_minutes}m</span>
                  </div>

                  {hasProgress && hasProgress.time_spent_minutes > 0 && (
                    <div className="flex items-center gap-1 text-primary-600">
                      <Clock className="h-4 w-4" />
                      <span>
                        {formatTime(hasProgress.time_spent_minutes)} spent
                      </span>
                    </div>
                  )}

                  <span className="capitalize text-gray-400">
                    {lesson.content_type}
                  </span>
                </div>

                {hasProgress?.notes && (
                  <div className="mt-2 p-2 bg-gray-50 rounded text-sm text-gray-600">
                    <strong>Note:</strong> {hasProgress.notes}
                  </div>
                )}

                {status !== 'completed' && (
                  <button
                    onClick={() => handleMarkComplete(lesson.id)}
                    disabled={updatingLesson === lesson.id}
                    className="mt-3 btn-primary text-sm disabled:opacity-50"
                  >
                    {updatingLesson === lesson.id
                      ? 'Updating...'
                      : 'Mark as Complete'}
                  </button>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default LessonList;