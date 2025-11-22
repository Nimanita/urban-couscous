// src/api/courses.js
import api from './axios';

export const coursesAPI = {
  // Get all courses
  getAllCourses: async () => {
    const response = await api.get('/courses');
    return response.data;
  },

  // Get course by ID
  getCourseById: async (courseId) => {
    const response = await api.get(`/courses/${courseId}`);
    return response.data;
  },

  // Get lessons for a course
  getCourseLessons: async (courseId) => {
    const response = await api.get(`/courses/${courseId}/lessons`);
    return response.data;
  },
};