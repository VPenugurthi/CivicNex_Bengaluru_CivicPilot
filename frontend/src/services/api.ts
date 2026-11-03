
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

export interface Incident {
  id?: number;
  title?: string;
  description?: string;
  status?: string;
  priority?: string;
  [key: string]: any;
}

export const civicApi = {
  async createIncident(data: Incident) {
    const response = await api.post('/incidents/', data);
    return response.data;
  },

  async getIncidents() {
    const response = await api.get('/incidents/');
    return response.data;
  },

  async getIncident(id: number) {
    const response = await api.get(`/incidents/${id}`);
    return response.data;
  },

  async updateIncident(id: number, data: Partial<Incident>) {
    const response = await api.patch(`/incidents/${id}`, data);
    return response.data;
  },

  async runInvestigation(id: number) {
    const response = await api.post(`/ai/investigate/${id}`);
    return response.data;
  },

  async getRelationships(id: number) {
    const response = await api.get(`/incidents/${id}/relationships`);
    return response.data;
  },

  async addAction(
    id: number,
    actionText: string,
    reasoning: string
  ) {
    const response = await api.post(`/incidents/${id}/actions`, {
      action_text: actionText,
      reasoning,
    });

    return response.data;
  },
};
