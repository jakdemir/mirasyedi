import axios from 'axios';
import { Estate, InheritanceResult, ApiResponse } from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add request interceptor for logging
api.interceptors.request.use(
    (config) => {
        console.log('Request:', {
            method: config.method?.toUpperCase(),
            url: config.url,
            data: config.data,
        });
        return config;
    },
    (error) => {
        console.error('Request Error:', error);
        return Promise.reject(error);
    }
);

// Add response interceptor for logging
api.interceptors.response.use(
    (response) => {
        console.log('Response:', {
            status: response.status,
            data: response.data,
        });
        return response;
    },
    (error) => {
        console.error('Response Error:', error.response || error);
        return Promise.reject(error);
    }
);

export const calculateInheritance = async (estate: Estate): Promise<ApiResponse<InheritanceResult>> => {
    try {
        console.log('Sending estate data:', estate);
        
        const response = await api.post<Estate>('/calculate-inheritance', estate);
        console.log('Raw response:', response);

        if (!response.data) {
            throw new Error('Empty response from server');
        }

        return {
            data: {
                estate: response.data
            }
        };
    } catch (error) {
        console.error('Error details:', error);
        if (axios.isAxiosError(error)) {
            const errorMessage = error.response?.data?.detail?.[0]?.msg || error.response?.data?.error || error.message || 'Server error';
            return {
                data: { estate: { total_value: estate.total_value, family_tree: {} } },
                error: errorMessage
            };
        }
        return {
            data: { estate: { total_value: estate.total_value, family_tree: {} } },
            error: 'An unexpected error occurred'
        };
    }
}; 