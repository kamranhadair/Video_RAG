"""Data models for video transcripts and chunks."""
from dataclasses import dataclass, asdict
from typing import List, Optional
import json

@dataclass
class TranscriptSegment:
    """Single segment from Whisper transcription."""
    text: str
    start: float  # seconds
    end: float    # seconds
    
    def to_dict(self):
        return asdict(self)

@dataclass
class DocumentChunk:
    """Chunked transcript with metadata."""
    chunk_id: str
    video_id: str
    text: str
    start_time: float
    end_time: float
    chunk_index: int
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

@dataclass
class VideoMetadata:
    """Metadata for processed video."""
    video_id: str
    url: str
    title: str
    duration: float  # seconds
    num_chunks: int
    processed_at: str  # ISO timestamp
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, path):
        with open(path, 'r') as f:
            return cls.from_dict(json.load(f))

@dataclass
class RAGResponse:
    """Response from RAG query."""
    answer: str
    sources: List[dict]  # [{text, start_time, end_time, similarity}]
    video_id: str
    
    def to_dict(self):
        return asdict(self)
