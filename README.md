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

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/Video_RAG.git
cd Video_RAG
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Run the App

```bash
streamlit run frontend/app.py
```

Open http://localhost:8501 in your browser.

## 💡 Usage

### Web Interface (Recommended)

1. Enter a YouTube URL in the sidebar
2. Click "Process Video"
3. Wait for processing (2-5 minutes depending on video length)
4. Ask questions in the chat interface

### Python API

```python
from backend.services import VideoRAGService

service = VideoRAGService()

# Process a video
video_id = service.ingest_video("https://www.youtube.com/watch?v=...")

# Query the video
response = service.query(video_id, "What is this video about?", use_langgraph=True)
print(response.answer)
print(response.sources)
```

### With Conversation Memory

```python
from backend.utils.conversation_memory import ConversationMemory

memory = ConversationMemory()

# First turn
r1 = service.query(video_id, "What's the main topic?")
memory.add_turn("What's the main topic?", r1.answer)

# Second turn (with context)
r2 = service.query(video_id, "Tell me more about that")
memory.add_turn("Tell me more about that", r2.answer)
```

## 📁 Project Structure

```
Video_RAG/
├── backend/
│   ├── agents/                 # LangGraph agents
│   │   ├── query_analyzer.py   # Intent classification
│   │   ├── retrieval_agent.py  # Semantic search
│   │   ├── answer_generator.py # Answer synthesis
│   │   └── validator_agent.py  # Quality validation
│   ├── workflows/              # LangGraph workflows
│   │   └── rag_graph.py        # Main orchestration
│   ├── core/                   # Core components
│   │   ├── video_downloader.py # YouTube audio extraction
│   │   ├── transcriber.py      # Whisper transcription
│   │   ├── chunker.py          # Semantic chunking
│   │   ├── vector_store.py     # FAISS indexing
│   │   └── llm_adapter.py      # LLM abstraction
│   ├── services/               # Service layer
│   │   ├── video_rag_service.py # Main facade
│   │   └── rag_pipeline.py     # Legacy pipeline
│   ├── models/                 # Data models
│   │   ├── document.py         # Chunk, Metadata
│   │   └── rag_state.py        # LangGraph state
│   ├── utils/                  # Utilities
│   │   └── conversation_memory.py # Multi-turn support
│   └── config.py               # Configuration
├── frontend/
│   └── app.py                  # Streamlit UI
├── data/                       # Generated at runtime
│   ├── faiss_indexes/          # Vector indices
│   ├── metadata/               # Video metadata
│   └── cache/                  # Audio files
├── bin/                        # FFmpeg binaries
├── requirements.txt
├── .env.example
└── README.md
```

## 🔧 Configuration

Edit `.env` to customize:

```env
# LLM Provider
LLM_PROVIDER=groq              # groq | ollama
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Whisper Model
WHISPER_MODEL=base             # tiny | base | small | medium | large
WHISPER_DEVICE=cpu             # cpu | cuda

# Chunking
CHUNK_SIZE=500                 # tokens
CHUNK_OVERLAP=100              # tokens

# Retrieval
TOP_K_RETRIEVAL=5
SIMILARITY_THRESHOLD=0.2
MAX_CONTEXT_LENGTH=4000
```

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

## 📚 Documentation

- **ENGINEERING_NOTES.md**: Design decisions and trade-offs
- **CONTRIBUTING.md**: Contribution guidelines

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- OpenAI Whisper for transcription
- Facebook AI Research for FAISS
- Sentence Transformers community
- Groq for fast inference
- LangChain/LangGraph teams

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Status**: ✅ Production Ready | LangGraph v1 | Tested with multiple videos
