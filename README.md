# 🎥 Video RAG - Chat with YouTube Videos

A production-ready Retrieval-Augmented Generation (RAG) system for conversational Q&A over YouTube videos with LangGraph orchestration.

## ✨ Features

- 🎬 **YouTube Integration**: Download and process any YouTube video
- 🎤 **Whisper Transcription**: Accurate speech-to-text with timestamps
- 🔍 **Semantic Search**: FAISS vector store with cosine similarity
- 🤖 **LangGraph Workflow**: Multi-agent orchestration with intent routing
- 💬 **Conversation Memory**: Multi-turn conversations with context
- ✅ **Answer Validation**: Confidence scoring and quality checks
- 📍 **Source Attribution**: Timestamp-preserved citations
- 🚀 **Production Ready**: Clean, tested, and deployable

## 🏗️ Architecture

```
User Query
    ↓
Query Analyzer (Intent Classification)
    ↓
Retrieval Agent (Semantic Search)
    ↓
Answer Generator (LLM Synthesis)
    ↓
Validator Agent (Quality Check)
    ↓
Response with Confidence & Sources
```

## 📋 Prerequisites

- Python 3.9+
- FFmpeg (included in `bin/` directory)
- Groq API key (or Ollama for local inference)

## 🎯 Key Components

### Query Analyzer
Classifies query intent (qa, summary, comparison) for intelligent routing.

### Retrieval Agent
Performs semantic search using FAISS with confidence scoring.

### Answer Generator
Synthesizes answers using LLM with strict anti-hallucination prompts.

### Validator Agent
Checks answer quality and assigns confidence scores.

## 📊 Performance

- **Query Processing**: ~2 seconds
- **Video Processing**: 2-5 minutes (depends on length and model)
- **Confidence Scoring**: Per-answer quality metrics
- **Multi-turn Support**: Full conversation history

## 🔐 Security

- API keys stored in `.env` (never committed)
- Input validation on YouTube URLs
- No external API calls except LLM provider
- Local FAISS indices (no cloud storage)

## 🙏 Acknowledgments

- OpenAI Whisper for transcription
- Facebook AI Research for FAISS
- Sentence Transformers community
- Groq for fast inference
- LangChain/LangGraph teams
