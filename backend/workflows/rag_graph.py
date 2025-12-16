"""LangGraph workflow for RAG."""
from langgraph.graph import StateGraph, END
from backend.models.rag_state import RAGState
from backend.agents import QueryAnalyzer, RetrievalAgent, AnswerGenerator, ValidatorAgent

class RAGGraph:
    """LangGraph workflow for RAG pipeline."""
    
    def __init__(self):
        self.query_analyzer = QueryAnalyzer()
        self.retrieval_agent = RetrievalAgent()
        self.answer_generator = AnswerGenerator()
        self.validator_agent = ValidatorAgent()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow."""
        workflow = StateGraph(RAGState)
        
        # Add nodes
        workflow.add_node("analyze_query", self.query_analyzer.analyze)
        workflow.add_node("retrieve", self.retrieval_agent.retrieve)
        workflow.add_node("generate_answer", self.answer_generator.generate)
        workflow.add_node("validate", self.validator_agent.validate)
        
        # Add edges
        workflow.set_entry_point("analyze_query")
        workflow.add_edge("analyze_query", "retrieve")
        workflow.add_edge("retrieve", "generate_answer")
        workflow.add_edge("generate_answer", "validate")
        workflow.add_edge("validate", END)
        
        return workflow.compile()
    
    def query(self, video_id: str, question: str, conversation_history: list = None) -> dict:
        """Execute RAG workflow."""
        initial_state: RAGState = {
            "query": question,
            "video_id": video_id,
            "intent": "",
            "retrieved_chunks": [],
            "final_answer": "",
            "sources": [],
            "conversation_history": conversation_history or [],
            "confidence": 0.0,
            "retry_count": 0
        }
        
        result = self.graph.invoke(initial_state)
        
        return {
            "answer": result["final_answer"],
            "sources": result["sources"],
            "intent": result["intent"],
            "confidence": result["confidence"]
        }
