import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const resumeAPI = {
  upload: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/resume/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  get: async (resumeId) => {
    const response = await api.get(`/resume/${resumeId}`);
    return response.data;
  },

  analyze: async (resumeId) => {
    const response = await api.post(`/resume/${resumeId}/analyze`);
    return response.data;
  },

  atsOptimize: async (resumeId, jobDescription = null) => {
    const response = await api.post(`/resume/${resumeId}/ats-optimize`, {
      job_description: jobDescription
    });
    return response.data;
  },

  matchJob: async (resumeId, jobDescription) => {
    const response = await api.post(`/resume/${resumeId}/match-job`, {
      job_description: jobDescription
    });
    return response.data;
  },

  getSuggestions: async (resumeId) => {
    const response = await api.get(`/resume/${resumeId}/suggestions`);
    return response.data;
  },

  delete: async (resumeId) => {
    const response = await api.delete(`/resume/${resumeId}`);
    return response.data;
  },

  improveFormat: async (resumeId) => {
    const response = await api.post(`/resume/${resumeId}/improve-format`);
    return response.data;
  },

  generate: async (resumeId, templateId, format = 'doc') => {
    const response = await api.post(
      `/resume/${resumeId}/generate?template_id=${templateId}&format=${format}`,
      {},
      {
        responseType: 'blob'
      }
    );
    return response.data;
  },

  // Version Management
  createVersion: async (resumeId, changeDescription = null) => {
    const response = await api.post(`/resume/${resumeId}/version`, {
      change_description: changeDescription
    });
    return response.data;
  },

  listVersions: async (resumeId) => {
    const response = await api.get(`/resume/${resumeId}/versions`);
    return response.data;
  },

  getVersion: async (resumeId, version) => {
    const response = await api.get(`/resume/${resumeId}/version/${version}`);
    return response.data;
  },

  updateResume: async (resumeId, industry = null, tags = null) => {
    const response = await api.put(`/resume/${resumeId}`, {
      industry,
      tags
    });
    return response.data;
  },

  listResumes: async (industry = null, tag = null) => {
    const params = {};
    if (industry) params.industry = industry;
    if (tag) params.tag = tag;
    const response = await api.get('/resumes', { params });
    return response.data;
  },

  // Cover Letter
  generateCoverLetter: async (resumeId, jobDescription, companyName = null, tone = 'professional', length = 'medium') => {
    const response = await api.post(`/resume/${resumeId}/cover-letter`, {
      job_description: jobDescription,
      company_name: companyName,
      tone,
      length
    });
    return response.data;
  },

  // Interview Preparation
  generateInterviewQuestions: async (resumeId, jobDescription, questionTypes = ['behavioral', 'technical', 'situational']) => {
    const response = await api.post(`/resume/${resumeId}/interview-questions`, {
      job_description: jobDescription,
      question_types: questionTypes
    });
    return response.data;
  },

  generateAnswer: async (resumeId, question, jobDescription = null) => {
    const response = await api.post(`/resume/${resumeId}/interview-answer`, {
      question,
      job_description: jobDescription
    });
    return response.data;
  },

  // Custom Template Generation
  generateCustom: async (resumeId, templateId, customizations, format = 'doc') => {
    const response = await api.post(
      `/resume/${resumeId}/generate-custom?format=${format}`,
      {
        template_id: templateId,
        customizations
      },
      {
        responseType: 'blob'
      }
    );
    return response.data;
  }
};

export const templateAPI = {
  list: async (industry = null) => {
    const params = industry ? { industry } : {};
    const response = await api.get('/templates', { params });
    return response.data;
  },

  get: async (templateId) => {
    const response = await api.get(`/templates/${templateId}`);
    return response.data;
  },

  listIndustries: async () => {
    const response = await api.get('/industries');
    return response.data;
  }
};

export const authAPI = {
  register: async (email, username, password) => {
    const response = await api.post('/auth/register', {
      email,
      username,
      password
    });
    return response.data;
  },

  login: async (email, password) => {
    const response = await api.post('/auth/login', {
      email,
      password
    });
    return response.data;
  },

  getCurrentUser: async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No token found');
    }
    const response = await api.get('/auth/me', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data;
  }
};

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
