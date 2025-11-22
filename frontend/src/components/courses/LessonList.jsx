// src/components/courses/LessonList.jsx
// src/components/courses/LessonList.jsx
import { CheckCircle2, Circle, Clock, PlayCircle, X } from 'lucide-react';
import { formatTime, getStatusColor, formatStatus, formatDate } from '../../utils/helpers';
import { useState } from 'react';
import { progressAPI } from '../../api/progress';

const ConfirmModal = ({ isOpen, onClose, onConfirm, lessonTitle, isLoading }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-md w-full p-6 shadow-2xl">
        <div className="flex items-start justify-between mb-4">
          <h3 className="text-xl font-bold text-gray-900">Confirm Completion</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
            disabled={isLoading}
          >
            <X className="h-5 w-5" />
          </button>
        </div>
        
        <p className="text-gray-600 mb-6">
          Are you sure you want to mark <strong>"{lessonTitle}"</strong> as complete?
        </p>
        
        <div className="flex gap-3">
          <button
            onClick={onClose}
            disabled={isLoading}
            className="flex-1 btn-secondary disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            disabled={isLoading}
            className="flex-1 btn-primary disabled:opacity-50"
          >
            {isLoading ? 'Marking Complete...' : 'Yes, Complete'}
          </button>
        </div>
      </div>
    </div>
  );
};

const LessonList = ({ lessons, onProgressUpdate }) => {
  const [updatingLesson, setUpdatingLesson] = useState(null);
  const [confirmModal, setConfirmModal] = useState({ isOpen: false, lesson: null });

  const handleMarkComplete = async () => {
    if (!confirmModal.lesson) return;
    
    const lessonId = confirmModal.lesson.id;
    setUpdatingLesson(lessonId);
    
    try {
      // Call API to mark lesson as complete
      await progressAPI.markLessonComplete(lessonId, 0);
      
      // Close modal
      setConfirmModal({ isOpen: false, lesson: null });
      
      // Trigger parent component to refresh data
      if (onProgressUpdate) {
        await onProgressUpdate();
      }
      
    } catch (error) {
      console.error('Failed to mark lesson complete:', error);
      alert('Failed to update lesson status. Please try again.');
    } finally {
      setUpdatingLesson(null);
    }
  };

  const openConfirmModal = (lesson) => {
    setConfirmModal({ isOpen: true, lesson });
  };

  const closeConfirmModal = () => {
    if (!updatingLesson) {
      setConfirmModal({ isOpen: false, lesson: null });
    }
  };

  return (
    <>
      <div className="space-y-3">
        {lessons.map((lesson) => {
          // Status is a direct property of lesson
          const status = lesson.status || 'not_started';
          const isCompleted = status === 'completed';
          const isUpdating = updatingLesson === lesson.id;

          return (
            <div
              key={lesson.id}
              className={`card hover:shadow-md transition-all ${
                isCompleted ? 'bg-green-50 border-green-200' : ''
              } ${isUpdating ? 'opacity-70 pointer-events-none' : ''}`}
            >
              <div className="flex items-start gap-4">
                {/* Status Icon */}
                <div className="flex-shrink-0 mt-1">
                  {isCompleted ? (
                    <CheckCircle2 className="h-6 w-6 text-green-600" />
                  ) : status === 'in_progress' ? (
                    <PlayCircle className="h-6 w-6 text-blue-500" />
                  ) : (
                    <Circle className="h-6 w-6 text-gray-300" />
                  )}
                </div>

                <div className="flex-1 min-w-0">
                  {/* Lesson Title and Status Badge */}
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <h4 className={`text-base font-semibold ${
                        isCompleted ? 'text-green-900 line-through' : 'text-gray-900'
                      }`}>
                        {lesson.title}
                      </h4>
                      <p className={`text-sm mt-1 ${
                        isCompleted ? 'text-green-700' : 'text-gray-600'
                      }`}>
                        {lesson.description}
                      </p>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap ${getStatusColor(
                        status
                      )}`}
                    >
                      {formatStatus(status)}
                    </span>
                  </div>

                  {/* Lesson Metadata */}
                  <div className="flex flex-wrap items-center gap-4 mt-3 text-sm">
                    <div className="flex items-center gap-1 text-gray-500">
                      <Clock className="h-4 w-4" />
                      <span>~{lesson.estimated_minutes}m</span>
                    </div>

                    {lesson.time_spent_minutes > 0 && (
                      <div className="flex items-center gap-1 text-primary-600 font-medium">
                        <Clock className="h-4 w-4" />
                        <span>
                          {formatTime(lesson.time_spent_minutes)} spent
                        </span>
                      </div>
                    )}

                    <span className="capitalize text-gray-400">
                      {lesson.content_type}
                    </span>
                  </div>

                  {/* Completion Info */}
                  {isCompleted && lesson.completed_at && (
                    <div className="mt-3 p-3 bg-green-100 border border-green-200 rounded-lg">
                      <div className="flex items-center gap-2">
                        <CheckCircle2 className="h-4 w-4 text-green-600" />
                        <span className="text-sm font-medium text-green-800">
                          ✓ Completed on {formatDate(lesson.completed_at)}
                        </span>
                      </div>
                    </div>
                  )}

                  {/* Notes */}
                  {lesson.notes && lesson.notes.trim() !== '' && (
                    <div className="mt-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                      <p className="text-sm text-blue-900">
                        <strong className="text-blue-700">Note:</strong> {lesson.notes}
                      </p>
                    </div>
                  )}

                  {/* Mark Complete Button - Only show if NOT completed */}
                  {!isCompleted && (
                    <button
                      onClick={() => openConfirmModal(lesson)}
                      disabled={isUpdating}
                      className="mt-4 btn-primary text-sm disabled:opacity-50 hover:shadow-md flex items-center gap-2"
                    >
                      {isUpdating ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                          Updating...
                        </>
                      ) : (
                        <>
                          <CheckCircle2 className="h-4 w-4" />
                          Mark as Complete
                        </>
                      )}
                    </button>
                  )}

                  {/* Already Completed Message */}
                  {isCompleted && (
                    <div className="mt-4 flex items-center gap-2 text-green-700">
                      <CheckCircle2 className="h-5 w-5" />
                      <span className="text-sm font-medium">This lesson is completed! 🎉</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <ConfirmModal
        isOpen={confirmModal.isOpen}
        onClose={closeConfirmModal}
        onConfirm={handleMarkComplete}
        lessonTitle={confirmModal.lesson?.title || ''}
        isLoading={!!updatingLesson}
      />
    </>
  );
};

export default LessonList;