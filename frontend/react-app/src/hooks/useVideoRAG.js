/**
 * Custom hook for Video RAG state management
 */
import { useState, useEffect, useCallback } from 'react';
import videoRAGAPI from '../services/api';

export const useVideoRAG = () => {
  const [videoId, setVideoId] = useState(null);
  const [status, setStatus] = useState('idle'); // idle | processing | ready | error
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState('');
  const [metadata, setMetadata] = useState(null);
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);

  // Poll status when processing
  useEffect(() => {
    if (status !== 'processing' || !videoId) return;

    const pollInterval = setInterval(async () => {
      try {
        const statusData = await videoRAGAPI.getStatus(videoId);
        setProgress(statusData.progress);
        setStage(statusData.stage);

        if (statusData.status === 'complete') {
          setStatus('ready');
          const meta = await videoRAGAPI.getMetadata(videoId);
          setMetadata(meta);
          clearInterval(pollInterval);
        } else if (statusData.status === 'error') {
          setStatus('error');
          setError(statusData.error);
          clearInterval(pollInterval);
        }
      } catch (err) {
        setError(err.message);
        setStatus('error');
        clearInterval(pollInterval);
      }
    }, 2000);

    return () => clearInterval(pollInterval);
  }, [status, videoId]);

  const ingestVideo = useCallback(async (url) => {
    try {
      setError(null);
      const response = await videoRAGAPI.ingestVideo(url);
      setVideoId(response.video_id);
      setStatus('processing');
      setMessages([]);
    } catch (err) {
      setError(err.message);
      setStatus('error');
    }
  }, []);

  const askQuestion = useCallback(async (question) => {
    if (!videoId) return;

    const userMessage = { role: 'user', content: question };
    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await videoRAGAPI.query(videoId, question);
      const assistantMessage = {
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage = {
        role: 'assistant',
        content: `Error: ${err.message}`,
        sources: [],
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  }, [videoId]);

  const reset = useCallback(() => {
    setVideoId(null);
    setStatus('idle');
    setProgress(0);
    setStage('');
    setMetadata(null);
    setMessages([]);
    setError(null);
  }, []);

  return {
    videoId,
    status,
    progress,
    stage,
    metadata,
    messages,
    error,
    ingestVideo,
    askQuestion,
    reset,
  };
};
