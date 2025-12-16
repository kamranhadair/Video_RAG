import React from 'react';
import { useVideoRag } from './hooks/useVideoRag';
import { VideoIngest } from './components/VideoIngest';
import { StatusView } from './components/StatusView';
import { ChatInterface } from './components/ChatInterface';
import './App.css';

function App() {
  const {
    videoId,
    status,
    progress,
    stage,
    chatHistory,
    loading,
    error,
    ingestVideo,
    askQuestion
  } = useVideoRag();

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🎥 Video RAG System</h1>
        <p>Minimal React Frontend</p>
      </header>

      <main className="app-content">
        <VideoIngest
          onIngest={ingestVideo}
          loading={loading}
        />

        <StatusView
          status={status}
          progress={progress}
          stage={stage}
          error={error}
        />

        <ChatInterface
          chatHistory={chatHistory}
          onAsk={askQuestion}
          loading={loading}
          disabled={status !== 'ready'}
        />
      </main>
    </div>
  );
}

export default App;
