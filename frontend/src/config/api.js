/**
 * API Configuration
 * Centralized configuration for API endpoints
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || '';

export const API_ENDPOINTS = {
  // Authentication
  LOGIN: '/api/v1/users/login',
  REGISTER: '/api/v1/users/register',
  ME: '/api/v1/users/me',
  UPDATE_PROFILE: '/api/v1/users/me',
  
  // Assessment
  ASSESSMENT_QUESTIONS: '/api/v1/assessment/questions',
  SUBMIT_ASSESSMENT: '/api/v1/assessment/submit',
  ASSESSMENT_RESULT: '/api/v1/assessment/result',
  
  // Content
  CONTENT_LIST: '/api/v1/content/',
  CONTENT_DETAIL: (id) => `/api/v1/content/${id}`,
  ADAPTIVE_CONTENT: (id) => `/api/v1/content/${id}/adaptive`,
  CONTENT_PROGRESS: (id) => `/api/v1/content/${id}/progress`,
  CONTENT_INTERACTION: (id) => `/api/v1/content/${id}/interaction`,
  RECOMMENDATIONS: '/api/v1/content/recommendations/personalized',
  
  // Analytics
  DASHBOARD_OVERVIEW: '/api/v1/analytics/dashboard/overview',
  USER_ANALYTICS: (id) => `/api/v1/analytics/user/${id}`,
  CONTENT_ANALYTICS: (id) => `/api/v1/analytics/content/${id}`,
};

export const getApiUrl = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`;
};

export default {
  API_BASE_URL,
  API_ENDPOINTS,
  getApiUrl,
};
