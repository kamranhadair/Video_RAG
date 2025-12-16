const API_BASE = 'http://localhost:8000/api';

export const apiClient = {
    async ingestVideo(url) {
        const response = await fetch(`${API_BASE}/ingest`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url }),
        });
        if (!response.ok) throw new Error('Ingest failed');
        return response.json();
    },

    async getStatus(videoId) {
        const response = await fetch(`${API_BASE}/status/${videoId}`);
        if (!response.ok) throw new Error('Status check failed');
        return response.json();
    },

    async askQuestion(videoId, question) {
        const response = await fetch(`${API_BASE}/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ video_id: videoId, question }),
        });
        if (!response.ok) throw new Error('Query failed');
        return response.json();
    }
};
