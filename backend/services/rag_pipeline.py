"""RAG pipeline for query processing."""
from typing import List, Tuple
from backend.models import DocumentChunk, RAGResponse
from backend.core import VectorStore, LLMAdapter

class RAGPipeline:
    """Retrieval-Augmented Generation pipeline."""
    
    def __init__(self, vector_store: VectorStore, llm: LLMAdapter):
        self.vector_store = vector_store
        self.llm = llm
    
    def query(
        self, 
        video_id: str, 
        question: str,
        top_k: int = 5,
        threshold: float = 0.3
    ) -> RAGResponse:
        """
        Process query using RAG.
        
        Steps:
        1. Retrieve relevant chunks from vector store
        2. Construct prompt with strict constraints
        3. Generate answer using LLM
        4. Parse and return response with sources
        """
        # Retrieve relevant chunks
        results = self.vector_store.search(
            video_id=video_id,
            query=question,
            top_k=top_k,
            threshold=threshold
        )
        
        if not results:
            return RAGResponse(
                answer="I couldn't find relevant information in the video to answer this question.",
                sources=[],
                video_id=video_id
            )
        
        # Construct prompt
        prompt = self._build_prompt(question, results)
        
        # Generate answer
        answer = self.llm.generate(prompt, max_tokens=500)
        
        # Format sources
        sources = [
            {
                'text': chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text,
                'start_time': chunk.start_time,
                'end_time': chunk.end_time,
                'similarity': similarity,
                'timestamp_url': self._format_timestamp(chunk.start_time)
            }
            for chunk, similarity in results
        ]
        
        return RAGResponse(
            answer=answer,
            sources=sources,
            video_id=video_id
        )
    
    def _build_prompt(
        self, 
        question: str, 
        results: List[Tuple[DocumentChunk, float]]
    ) -> str:
        """
        Build prompt with strict anti-hallucination constraints.
        
        Prompt engineering strategy:
        - Explicit instruction to only use provided context
        - Include timestamps in context for reference
        - Request citation of timestamps in answer
        - Penalize speculation
        """
        context_parts = []
        for i, (chunk, _) in enumerate(results, 1):
            timestamp = self._format_timestamp(chunk.start_time)
            context_parts.append(
                f"[{i}] (Timestamp: {timestamp})\n{chunk.text}"
            )
        
        context = "\n\n".join(context_parts)
        
        prompt = f"""You are a video content assistant. Answer the question using ONLY the information from the video transcript provided below.

STRICT RULES:
1. Only use information explicitly stated in the transcript
2. If the answer is not in the transcript, say "This information is not covered in the video"
3. Reference timestamps when possible (e.g., "At 2:30, the speaker mentions...")
4. Do not add external knowledge or speculation
5. Be concise and direct

TRANSCRIPT EXCERPTS:
{context}

QUESTION: {question}

ANSWER:"""
        
        return prompt
    
    def _format_timestamp(self, seconds: float) -> str:
        """Format seconds as MM:SS or HH:MM:SS."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"
