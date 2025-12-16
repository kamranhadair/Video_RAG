"""Answer generator agent."""
from backend.models.rag_state import RAGState
from backend.core import create_llm_adapter
from backend.config import config

class AnswerGenerator:
    """Generates answer from retrieved chunks."""
    
    def __init__(self):
        self.llm = create_llm_adapter(
            provider=config.LLM_PROVIDER,
            api_key=config.GROQ_API_KEY,
            model=config.GROQ_MODEL
        )
    
    def generate(self, state: RAGState) -> RAGState:
        """Generate answer from retrieved chunks."""
        if not state["retrieved_chunks"]:
            state["final_answer"] = "I couldn't find relevant information in the video to answer this question."
            state["sources"] = []
            return state
        
        # Build prompt
        context_parts = []
        for i, chunk in enumerate(state["retrieved_chunks"], 1):
            timestamp = self._format_timestamp(chunk.start_time)
            context_parts.append(f"[{i}] (Timestamp: {timestamp})\n{chunk.text}")
        
        context = "\n\n".join(context_parts)
        
        prompt = f"""You are a video content assistant. Answer using ONLY the transcript.

STRICT RULES:
1. Only use information explicitly stated
2. If not in transcript, say "not covered in video"
3. Reference timestamps when possible
4. No external knowledge or speculation

TRANSCRIPT EXCERPTS:
{context}

QUESTION: {state['query']}

ANSWER:"""
        
        answer = self.llm.generate(prompt, max_tokens=500)
        state["final_answer"] = answer
        
        # Format sources
        sources = []
        for chunk in state["retrieved_chunks"]:
            sources.append({
                'text': chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text,
                'start_time': chunk.start_time,
                'end_time': chunk.end_time,
                'timestamp_url': self._format_timestamp(chunk.start_time)
            })
        state["sources"] = sources
        
        return state
    
    def _format_timestamp(self, seconds: float) -> str:
        """Format seconds as MM:SS or HH:MM:SS."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"
