"""FAISS-based vector store with metadata management."""
import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from backend.models import DocumentChunk

class VectorStore:
    """Manages FAISS index and chunk metadata."""
    
    def __init__(self, embedding_model: str, dimension: int, index_dir: Path):
        self.embedding_model = SentenceTransformer(embedding_model)
        self.dimension = dimension
        self.index_dir = index_dir
        self.index_dir.mkdir(parents=True, exist_ok=True)
    
    def create_index(self, video_id: str, chunks: List[DocumentChunk]):
        """
        Create FAISS index for video chunks.
        
        Stores:
        - FAISS index: {video_id}.faiss
        - Metadata: {video_id}_metadata.pkl (list of DocumentChunk)
        """
        # Generate embeddings
        texts = [chunk.text for chunk in chunks]
        embeddings = self.embedding_model.encode(texts, show_progress_bar=False)
        embeddings = np.array(embeddings).astype('float32')
        
        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index (IndexFlatIP for cosine similarity)
        index = faiss.IndexFlatIP(self.dimension)
        index.add(embeddings)
        
        # Save index and metadata
        index_path = self.index_dir / f"{video_id}.faiss"
        metadata_path = self.index_dir / f"{video_id}_metadata.pkl"
        
        faiss.write_index(index, str(index_path))
        with open(metadata_path, 'wb') as f:
            pickle.dump(chunks, f)
    
    def search(
        self, 
        video_id: str, 
        query: str, 
        top_k: int = 5,
        threshold: float = 0.3
    ) -> List[Tuple[DocumentChunk, float]]:
        """
        Search for relevant chunks.
        
        Returns:
            List of (DocumentChunk, similarity_score) tuples
        """
        index_path = self.index_dir / f"{video_id}.faiss"
        metadata_path = self.index_dir / f"{video_id}_metadata.pkl"
        
        if not index_path.exists():
            raise ValueError(f"Index not found for video_id: {video_id}")
        
        # Load index and metadata
        index = faiss.read_index(str(index_path))
        with open(metadata_path, 'rb') as f:
            chunks = pickle.load(f)
        
        # Encode query
        query_embedding = self.embedding_model.encode([query])[0]
        query_embedding = np.array([query_embedding]).astype('float32')
        faiss.normalize_L2(query_embedding)
        
        # Search
        similarities, indices = index.search(query_embedding, top_k)
        
        # Filter by threshold and return results
        results = []
        for idx, similarity in zip(indices[0], similarities[0]):
            if similarity >= threshold:
                results.append((chunks[idx], float(similarity)))
        
        return results
    
    def index_exists(self, video_id: str) -> bool:
        """Check if index exists for video."""
        index_path = self.index_dir / f"{video_id}.faiss"
        return index_path.exists()
