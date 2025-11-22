// src/api/dashboard.js
import api from './axios';

export const dashboardAPI = {
  // Get dashboard data
  getDashboard: async () => {
    const response = await api.get('/dashboard/');
    return response.data;
  },

  // Get time series data
  getTimeSeries: async (days = 30) => {
    const response = await api.get(`/dashboard/timeseries?days=${days}`);
    return response.data;
  },

  // Get completion distribution
  getDistribution: async () => {
    const response = await api.get('/dashboard/distribution/');
    return response.data;
  },
    // Get recommendations
  getRecommendations: async () => {
    const response = await api.get('/report/recommendations/');
    return response.data;
  },

  // Generate new recommendations
  generateRecommendations: async (limit = 5) => {
    const response = await api.post('/report/recommendations/generate/', { limit });
    return response.data;
  },

  // Dismiss a recommendation
  dismissRecommendation: async (recommendationId) => {
    const response = await api.post(`/report/recommendations/${recommendationId}/dismiss`);
    return response.data;
  },

};

