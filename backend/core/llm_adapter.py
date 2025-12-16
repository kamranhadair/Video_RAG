"""LLM adapter supporting Groq and Ollama."""
from abc import ABC, abstractmethod
from typing import Optional
import requests
from groq import Groq

class LLMAdapter(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate response from prompt."""
        pass

class GroqAdapter(LLMAdapter):
    """Groq API adapter."""
    
    def __init__(self, api_key: str, model: str = "llama-3.1-70b-versatile"):
        self.client = Groq(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.1,  # Low temperature for factual responses
        )
        return response.choices[0].message.content

class OllamaAdapter(LLMAdapter):
    """Ollama local API adapter."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1"):
        self.base_url = base_url.rstrip('/')
        self.model = model
    
    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": max_tokens
                }
            }
        )
        response.raise_for_status()
        return response.json()["response"]

def create_llm_adapter(provider: str, **kwargs) -> LLMAdapter:
    """Factory function to create LLM adapter."""
    if provider == "groq":
        return GroqAdapter(
            api_key=kwargs.get("api_key"),
            model=kwargs.get("model", "llama-3.1-70b-versatile")
        )
    elif provider == "ollama":
        return OllamaAdapter(
            base_url=kwargs.get("base_url", "http://localhost:11434"),
            model=kwargs.get("model", "llama3.1")
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
