"""Retrieval agent for semantic search."""
from backend.models.rag_state import RAGState
from backend.core import VectorStore
from backend.config import config

class RetrievalAgent:
    """Retrieves relevant chunks from vector store."""
    
    def __init__(self):
        self.vector_store = VectorStore(
            embedding_model=config.EMBEDDING_MODEL,
            dimension=config.EMBEDDING_DIMENSION,
            index_dir=config.FAISS_DIR
        )
    
    def retrieve(self, state: RAGState) -> RAGState:
        """Retrieve relevant chunks."""
        results = self.vector_store.search(
            video_id=state["video_id"],
            query=state["query"],
            top_k=config.TOP_K_RETRIEVAL,
            threshold=config.SIMILARITY_THRESHOLD
        )
        
        if results:
            chunks, similarities = zip(*results)
            state["retrieved_chunks"] = list(chunks)
            state["confidence"] = float(similarities[0]) if similarities else 0.0
        else:
            state["retrieved_chunks"] = []
            state["confidence"] = 0.0
        
        return state
