"""Conversation memory management."""
from typing import List, Dict
from datetime import datetime

class ConversationMemory:
    """Manages conversation history for context-aware retrieval."""
    
    def __init__(self, max_history: int = 5):
        self.history: List[Dict] = []
        self.max_history = max_history
    
    def add_turn(self, query: str, answer: str, intent: str = ""):
        """Add a query-answer pair to history."""
        self.history.append({
            "query": query,
            "answer": answer,
            "intent": intent,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent turns
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_context(self, k: int = 3) -> str:
        """Get last k turns as context string."""
        recent = self.history[-k:] if len(self.history) >= k else self.history
        
        if not recent:
            return ""
        
        context_parts = []
        for turn in recent:
            context_parts.append(f"Q: {turn['query']}\nA: {turn['answer']}")
        
        return "\n\n".join(context_parts)
    
    def clear(self):
        """Clear conversation history."""
        self.history = []
    
    def get_history(self) -> List[Dict]:
        """Get full conversation history."""
        return self.history.copy()
