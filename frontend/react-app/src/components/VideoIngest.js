import React, { useState } from 'react';

export const VideoIngest = ({ onIngest, loading }) => {
    const [url, setUrl] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (url.trim()) {
            onIngest(url);
        }
    };

    return (
        <div className="card">
            <h2>1. Ingest Video</h2>
            <form onSubmit={handleSubmit} className="ingest-form">
                <input
                    type="url"
                    placeholder="Enter YouTube URL"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    disabled={loading}
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Processing...' : 'Start Processing'}
                </button>
            </form>
        </div>
    );
};
