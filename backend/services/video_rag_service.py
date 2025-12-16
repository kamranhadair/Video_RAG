"""Main service facade for video RAG operations."""
from datetime import datetime
from typing import Optional, Dict
from pathlib import Path
import threading
from backend.config import config
from backend.models import VideoMetadata, RAGResponse
from backend.core import (
    VideoDownloader, 
    Transcriber, 
    TranscriptChunker, 
    VectorStore,
    create_llm_adapter
)
from backend.services.rag_pipeline import RAGPipeline
from backend.workflows import RAGGraph

class VideoRAGService:
    """Facade for all video RAG operations."""
    
    def __init__(self):
        # Initialize components
        self.downloader = VideoDownloader(config.CACHE_DIR)
        self.transcriber = Transcriber(
            model_size=config.WHISPER_MODEL,
            device=config.WHISPER_DEVICE
        )
        self.chunker = TranscriptChunker(
            chunk_size=config.CHUNK_SIZE,
            overlap=config.CHUNK_OVERLAP
        )
        self.vector_store = VectorStore(
            embedding_model=config.EMBEDDING_MODEL,
            dimension=config.EMBEDDING_DIMENSION,
            index_dir=config.FAISS_DIR
        )
        self.llm = create_llm_adapter(
            provider=config.LLM_PROVIDER,
            api_key=config.GROQ_API_KEY,
            model=config.GROQ_MODEL if config.LLM_PROVIDER == "groq" else config.OLLAMA_MODEL,
            base_url=config.OLLAMA_BASE_URL
        )
        self.rag_pipeline = RAGPipeline(self.vector_store, self.llm)
        self.rag_graph = RAGGraph()
        
        # Processing status tracking
        self._processing_status: Dict[str, dict] = {}
        self._lock = threading.Lock()
    
    def ingest_video(self, url: str) -> str:
        """Start video ingestion process."""
        audio_path, metadata = self.downloader.download_audio(url)
        video_id = metadata['video_id']
        
        with self._lock:
            self._processing_status[video_id] = {
                'status': 'processing',
                'stage': 'downloading',
                'progress': 0.1,
                'metadata': metadata
            }
        
        thread = threading.Thread(
            target=self._process_video,
            args=(video_id, audio_path, metadata)
        )
        thread.daemon = True
        thread.start()
        
        return video_id
    
    def _process_video(self, video_id: str, audio_path: str, metadata: dict):
        """Background processing of video."""
        try:
            self._update_status(video_id, 'transcribing', 0.3)
            segments = self.transcriber.transcribe(audio_path)
            
            self._update_status(video_id, 'chunking', 0.6)
            chunks = self.chunker.chunk(segments, video_id)
            
            self._update_status(video_id, 'indexing', 0.8)
            self.vector_store.create_index(video_id, chunks)
            
            video_metadata = VideoMetadata(
                video_id=video_id,
                url=metadata['url'],
                title=metadata['title'],
                duration=metadata['duration'],
                num_chunks=len(chunks),
                processed_at=datetime.now().isoformat()
            )
            metadata_path = config.METADATA_DIR / f"{video_id}.json"
            video_metadata.save(metadata_path)
            
            self._update_status(video_id, 'complete', 1.0)
            
        except Exception as e:
            self._update_status(video_id, 'error', 0.0, error=str(e))
    
    def get_status(self, video_id: str) -> dict:
        """Get processing status for video."""
        with self._lock:
            return self._processing_status.get(video_id, {
                'status': 'unknown',
                'stage': 'unknown',
                'progress': 0.0
            })
    
    def query(self, video_id: str, question: str, use_langgraph: bool = True) -> RAGResponse:
        """Query video content."""
        if not self.vector_store.index_exists(video_id):
            raise ValueError(f"Video {video_id} not processed or not found")
        
        if use_langgraph:
            result = self.rag_graph.query(video_id, question)
            return RAGResponse(
                answer=result["answer"],
                sources=result["sources"],
                video_id=video_id
            )
        else:
            return self.rag_pipeline.query(
                video_id=video_id,
                question=question,
                top_k=config.TOP_K_RETRIEVAL,
                threshold=config.SIMILARITY_THRESHOLD
            )
    
    def get_metadata(self, video_id: str) -> Optional[VideoMetadata]:
        """Get video metadata."""
        metadata_path = config.METADATA_DIR / f"{video_id}.json"
        if not metadata_path.exists():
            return None
        return VideoMetadata.load(metadata_path)
    
    def _update_status(self, video_id: str, stage: str, progress: float, error: str = None):
        """Update processing status."""
        with self._lock:
            if video_id in self._processing_status:
                self._processing_status[video_id].update({
                    'stage': stage,
                    'progress': progress,
                    'status': 'error' if error else ('complete' if stage == 'complete' else 'processing'),
                    'error': error
                })
