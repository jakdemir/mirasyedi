import axios from 'axios';
import { InheritanceRequest, InheritanceResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
});

export const calculateInheritance = async (request: InheritanceRequest): Promise<InheritanceResponse> => {
    try {
        const response = await api.post<InheritanceResponse>('/calculate', request);
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            const errorMessage = error.response?.data?.detail || 'Failed to calculate inheritance';
            console.error('API Error:', error.response?.data);
            throw new Error(errorMessage);
        }
        throw error;
    }
}; 