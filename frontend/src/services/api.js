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
  }
};

export const templateAPI = {
  list: async () => {
    const response = await api.get('/templates');
    return response.data;
  },

  get: async (templateId) => {
    const response = await api.get(`/templates/${templateId}`);
    return response.data;
  }
};

export default api;
