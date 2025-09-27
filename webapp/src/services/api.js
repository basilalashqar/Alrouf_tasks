import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`Response from ${response.config.url}:`, response.status);
    return response;
  },
  (error) => {
    console.error('Response error:', error);
    
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.message || error.response.data?.detail || 'Server error';
      throw new Error(message);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('No response from server. Please check if the backend is running.');
    } else {
      // Something else happened
      throw new Error(error.message || 'Network error');
    }
  }
);

// Quotation Service API
export const quotationAPI = {
  generateQuotation: async (quotationData) => {
    try {
      const response = await api.post('/quote', quotationData);
      return response.data;
    } catch (error) {
      console.error('Error generating quotation:', error);
      throw error;
    }
  },

  getQuotation: async (quotationId) => {
    try {
      const response = await api.get(`/quote/${quotationId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching quotation:', error);
      throw error;
    }
  },

  listQuotations: async () => {
    try {
      const response = await api.get('/quotes');
      return response.data;
    } catch (error) {
      console.error('Error listing quotations:', error);
      throw error;
    }
  }
};

// RAG Knowledge Base API
export const ragAPI = {
  query: async (queryData) => {
    try {
      const response = await api.post('/rag/query', queryData);
      return response.data;
    } catch (error) {
      console.error('Error querying RAG system:', error);
      throw error;
    }
  },

  getDocuments: async () => {
    try {
      const response = await api.get('/rag/documents');
      return response.data;
    } catch (error) {
      console.error('Error fetching documents:', error);
      throw error;
    }
  },

  addDocument: async (documentData) => {
    try {
      const response = await api.post('/rag/documents', documentData);
      return response.data;
    } catch (error) {
      console.error('Error adding document:', error);
      throw error;
    }
  },

  getStats: async () => {
    try {
      const response = await api.get('/rag/stats');
      return response.data;
    } catch (error) {
      console.error('Error fetching RAG stats:', error);
      throw error;
    }
  }
};

// Health Check API
export const healthAPI = {
  check: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  },

  checkQuotationService: async () => {
    try {
      const response = await api.get('/health/quotation');
      return response.data;
    } catch (error) {
      console.error('Quotation service health check failed:', error);
      throw error;
    }
  },

  checkRAGService: async () => {
    try {
      const response = await api.get('/health/rag');
      return response.data;
    } catch (error) {
      console.error('RAG service health check failed:', error);
      throw error;
    }
  }
};

// Utility functions
export const utils = {
  formatCurrency: (amount, currency = 'SAR') => {
    return new Intl.NumberFormat('en-SA', {
      style: 'currency',
      currency: currency,
    }).format(amount);
  },

  formatDate: (date) => {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(new Date(date));
  },

  formatConfidence: (confidence) => {
    if (confidence >= 90) return { level: 'Excellent', color: '#10b981' };
    if (confidence >= 80) return { level: 'Good', color: '#3b82f6' };
    if (confidence >= 70) return { level: 'Fair', color: '#f59e0b' };
    return { level: 'Poor', color: '#ef4444' };
  },

  formatResponseTime: (time) => {
    if (time < 1000) return `${time}ms`;
    return `${(time / 1000).toFixed(1)}s`;
  }
};

export default api;
