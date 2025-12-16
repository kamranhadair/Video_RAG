"""Validator agent for answer quality checking."""
from backend.models.rag_state import RAGState
from backend.core import create_llm_adapter
from backend.config import config

class ValidatorAgent:
    """Validates answer quality and confidence."""
    
    def __init__(self):
        self.llm = create_llm_adapter(
            provider=config.LLM_PROVIDER,
            api_key=config.GROQ_API_KEY,
            model=config.GROQ_MODEL
        )
    
    def validate(self, state: RAGState) -> RAGState:
        """Validate answer quality."""
        if not state["final_answer"] or state["confidence"] < 0.2:
            state["confidence"] = 0.0
            return state
        
        # Check if answer contains "not covered" or similar phrases
        answer_lower = state["final_answer"].lower()
        if any(phrase in answer_lower for phrase in ["not covered", "not found", "not mentioned", "no information"]):
            state["confidence"] = 0.1
        else:
            # Confidence based on retrieval score
            state["confidence"] = min(state["confidence"], 0.95)
        
        return state
