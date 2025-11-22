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
};