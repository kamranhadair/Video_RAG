"""FastAPI backend for decoupled frontend architecture."""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from backend.services import VideoRAGService

app = FastAPI(
    title="Video RAG API",
    description="Multimodal RAG system for YouTube videos",
    version="1.0.0"
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
service = VideoRAGService()

# Request/Response models
class IngestRequest(BaseModel):
    url: HttpUrl

class IngestResponse(BaseModel):
    video_id: str
    status: str

class StatusResponse(BaseModel):
    video_id: str
    status: str
    stage: str
    progress: float
    error: Optional[str] = None
    metadata: Optional[dict] = None

class QueryRequest(BaseModel):
    video_id: str
    question: str

class Source(BaseModel):
    text: str
    start_time: float
    end_time: float
    similarity: float
    timestamp_url: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    video_id: str

class MetadataResponse(BaseModel):
    video_id: str
    url: str
    title: str
    duration: float
    num_chunks: int
    processed_at: str

# Endpoints
@app.post("/api/ingest", response_model=IngestResponse)
async def ingest_video(request: IngestRequest):
    """
    Start video ingestion process.
    
    Returns video_id for tracking.
    """
    try:
        video_id = service.ingest_video(str(request.url))
        return IngestResponse(video_id=video_id, status="processing")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status/{video_id}", response_model=StatusResponse)
async def get_status(video_id: str):
    """Get processing status for video."""
    status = service.get_status(video_id)
    
    if status.get('status') == 'unknown':
        raise HTTPException(status_code=404, detail="Video not found")
    
    return StatusResponse(
        video_id=video_id,
        status=status.get('status', 'unknown'),
        stage=status.get('stage', 'unknown'),
        progress=status.get('progress', 0.0),
        error=status.get('error'),
        metadata=status.get('metadata')
    )

@app.post("/api/query", response_model=QueryResponse)
async def query_video(request: QueryRequest):
    """Query video content."""
    try:
        response = service.query(request.video_id, request.question)
        return QueryResponse(
            answer=response.answer,
            sources=[Source(**s) for s in response.sources],
            video_id=response.video_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metadata/{video_id}", response_model=MetadataResponse)
async def get_metadata(video_id: str):
    """Get video metadata."""
    metadata = service.get_metadata(video_id)
    
    if not metadata:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return MetadataResponse(**metadata.to_dict())

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
