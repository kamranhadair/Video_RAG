/**
 * API client for Video RAG backend
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const videoRAGAPI = {
  /**
   * Ingest a YouTube video
   * @param {string} url - YouTube URL
   * @returns {Promise<{video_id: string, status: string}>}
   */
  ingestVideo: async (url) => {
    const response = await api.post('/api/ingest', { url });
    return response.data;
  },

  /**
   * Get processing status
   * @param {string} videoId
   * @returns {Promise<{status: string, stage: string, progress: number}>}
   */
  getStatus: async (videoId) => {
    const response = await api.get(`/api/status/${videoId}`);
    return response.data;
  },

  /**
   * Query video content
   * @param {string} videoId
   * @param {string} question
   * @returns {Promise<{answer: string, sources: Array}>}
   */
  query: async (videoId, question) => {
    const response = await api.post('/api/query', { video_id: videoId, question });
    return response.data;
  },

  /**
   * Get video metadata
   * @param {string} videoId
   * @returns {Promise<{title: string, duration: number, num_chunks: number}>}
   */
  getMetadata: async (videoId) => {
    const response = await api.get(`/api/metadata/${videoId}`);
    return response.data;
  },
};

export default videoRAGAPI;
