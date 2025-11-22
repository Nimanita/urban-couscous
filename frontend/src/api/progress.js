// src/api/progress.js
import api from './axios';

export const progressAPI = {
  // Get all progress for student
  getProgress: async () => {
    const response = await api.get('/report');
    return response.data;
  },

  // Update progress
  updateProgress: async (progressData) => {
    const response = await api.post('/report/update', progressData);
    return response.data;
  },

  // Mark lesson as complete
  markLessonComplete: async (lessonId, timeSpent = 0) => {
    const response = await api.post(`/report/complete/${lessonId}`, {
      time_spent: timeSpent,
    });
    return response.data;
  },
};