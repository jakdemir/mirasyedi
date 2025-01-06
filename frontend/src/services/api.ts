import axios from 'axios';
import { InheritanceRequest, InheritanceResponse, RelativeType } from '../types';

const API_BASE_URL = 'http://localhost:8000';  // FastAPI default port

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const inheritanceApi = {
  // Get available relative types
  getRelativeTypes: async (): Promise<RelativeType[]> => {
    const response = await api.get('/relative-types');
    return response.data;
  },

  // Calculate inheritance distribution
  calculateInheritance: async (request: InheritanceRequest): Promise<InheritanceResponse> => {
    const response = await api.post('/calculate', request);
    return response.data;
  },
};

export default inheritanceApi; 