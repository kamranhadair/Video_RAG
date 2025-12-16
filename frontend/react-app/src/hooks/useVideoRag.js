import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '../api/client';

export const useVideoRag = () => {
    const [videoId, setVideoId] = useState(null);
    const [status, setStatus] = useState('idle'); // idle, processing, ready, error
    const [progress, setProgress] = useState(0);
    const [stage, setStage] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const ingestVideo = async (url) => {
        try {
            setLoading(true);
            setError(null);
            const { video_id } = await apiClient.ingestVideo(url);
            setVideoId(video_id);
            setStatus('processing');
        } catch (err) {
            setError(err.message);
            setStatus('error');
        } finally {
            setLoading(false);
        }
    };

    const askQuestion = async (question) => {
        if (!videoId) return;

        // Optimistic update
        const userMsg = { role: 'user', content: question };
        setChatHistory(prev => [...prev, userMsg]);

        try {
            setLoading(true);
            const response = await apiClient.askQuestion(videoId, question);
            const botMsg = {
                role: 'assistant',
                content: response.answer,
                sources: response.sources
            };
            setChatHistory(prev => [...prev, botMsg]);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    // Polling logic
    useEffect(() => {
        let pollInterval;

        if (videoId && status === 'processing') {
            pollInterval = setInterval(async () => {
                try {
                    const data = await apiClient.getStatus(videoId);
                    setStatus(data.status);
                    setProgress(data.progress);
                    setStage(data.stage);

                    if (data.status === 'ready' || data.status === 'error') {
                        clearInterval(pollInterval);
                    }
                } catch (err) {
                    console.error('Polling error:', err);
                }
            }, 2000);
        }

        return () => clearInterval(pollInterval);
    }, [videoId, status]);

    return {
        videoId,
        status,
        progress,
        stage,
        chatHistory,
        loading,
        error,
        ingestVideo,
        askQuestion
    };
};
