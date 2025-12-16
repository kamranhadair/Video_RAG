import React, { useState, useRef, useEffect } from 'react';

export const ChatInterface = ({ chatHistory, onAsk, loading, disabled }) => {
    const [question, setQuestion] = useState('');
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [chatHistory]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (question.trim()) {
            onAsk(question);
            setQuestion('');
        }
    };

    if (disabled) return null;

    return (
        <div className="card chat-card">
            <h2>3. Chat with Video</h2>

            <div className="chat-history">
                {chatHistory.length === 0 && (
                    <div className="empty-state">Ask a question to get started...</div>
                )}

                {chatHistory.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.role}`}>
                        <div className="message-content">{msg.content}</div>

                        {msg.sources && (
                            <div className="sources">
                                <h4>Sources:</h4>
                                {msg.sources.map((source, sIdx) => (
                                    <div key={sIdx} className="source-item">
                                        <span className="timestamp">[{source.timestamp_url}]</span>
                                        <span className="source-text">{source.text}</span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
                <div ref={bottomRef} />
            </div>

            <form onSubmit={handleSubmit} className="chat-input-form">
                <input
                    type="text"
                    placeholder="Ask a question about the video..."
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    disabled={loading}
                />
                <button type="submit" disabled={loading || !question.trim()}>
                    Send
                </button>
            </form>
        </div>
    );
};
