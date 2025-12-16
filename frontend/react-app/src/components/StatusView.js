import React from 'react';

export const StatusView = ({ status, progress, stage, error }) => {
    if (status === 'idle') return null;

    return (
        <div className="card">
            <h2>2. Processing Status</h2>

            {error && <div className="error">Error: {error}</div>}

            <div className="status-container">
                <div className="status-header">
                    <span className="status-badge">{status.toUpperCase()}</span>
                    <span>{stage}</span>
                </div>

                <div className="progress-bar">
                    <div
                        className="progress-fill"
                        style={{ width: `${progress * 100}%` }}
                    />
                </div>

                <div className="progress-text">
                    {Math.round(progress * 100)}% Complete
                </div>
            </div>
        </div>
    );
};
