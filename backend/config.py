"""Configuration management with environment variable support."""
import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Config:
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    FAISS_DIR: Path = DATA_DIR / "faiss_indexes"
    METADATA_DIR: Path = DATA_DIR / "metadata"
    CACHE_DIR: Path = DATA_DIR / "cache"
    
    # LLM Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")  # groq | ollama
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    
    # Embedding Configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    EMBEDDING_DIMENSION: int = 384  # all-MiniLM-L6-v2 dimension
    
    # Transcription Configuration
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")  # tiny, base, small, medium, large
    WHISPER_DEVICE: str = os.getenv("WHISPER_DEVICE", "cpu")  # cpu | cuda
    
    # Chunking Configuration
    CHUNK_SIZE: int = 500  # tokens (roughly 375 words)
    CHUNK_OVERLAP: int = 100  # tokens
    
    # RAG Configuration
    TOP_K_RETRIEVAL: int = 5
    SIMILARITY_THRESHOLD: float = 0.2
    MAX_CONTEXT_LENGTH: int = 4000  # tokens for LLM context
    
    def __post_init__(self):
        """Create directories if they don't exist."""
        for dir_path in [self.FAISS_DIR, self.METADATA_DIR, self.CACHE_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)

config = Config()
