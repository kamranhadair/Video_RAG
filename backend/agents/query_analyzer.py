"""Query analyzer agent for intent classification."""
from backend.models.rag_state import RAGState

class QueryAnalyzer:
    """Analyzes query and classifies intent."""
    
    def analyze(self, state: RAGState) -> RAGState:
        """Classify query intent."""
        query = state["query"].lower()
        
        # Simple intent classification
        if any(word in query for word in ["summarize", "summary", "overview", "main points"]):
            intent = "summary"
        elif any(word in query for word in ["compare", "difference", "similar", "vs"]):
            intent = "comparison"
        else:
            intent = "qa"
        
        state["intent"] = intent
        return state
