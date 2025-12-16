"""Streamlit frontend for Video RAG system."""
import streamlit as st
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services import VideoRAGService
from backend.models import RAGResponse
from backend.utils.conversation_memory import ConversationMemory

st.set_page_config(
    page_title="Chat with Video",
    page_icon="🎥",
    layout="wide"
)

@st.cache_resource
def get_service():
    return VideoRAGService()

service = get_service()

if 'video_id' not in st.session_state:
    st.session_state.video_id = None
if 'status' not in st.session_state:
    st.session_state.status = 'idle'
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'metadata' not in st.session_state:
    st.session_state.metadata = None
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationMemory()

st.title("🎥 Chat with Video")
st.markdown("Ask questions about YouTube videos using AI-powered retrieval")

with st.sidebar:
    st.header("Video Input")
    
    url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        disabled=st.session_state.status == 'processing'
    )
    
    if st.button("Process Video", disabled=st.session_state.status == 'processing'):
        if url:
            try:
                video_id = service.ingest_video(url)
                st.session_state.video_id = video_id
                st.session_state.status = 'processing'
                st.session_state.messages = []
                st.session_state.memory.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a YouTube URL")
    
    if st.session_state.status == 'processing':
        st.divider()
        st.subheader("Processing...")
        
        status = service.get_status(st.session_state.video_id)
        progress = status.get('progress', 0.0)
        st.progress(progress)
        
        stage = status.get('stage', 'unknown')
        stage_emoji = {
            'downloading': '⬇️',
            'transcribing': '🎤',
            'chunking': '✂️',
            'indexing': '📊',
            'complete': '✅'
        }
        st.write(f"{stage_emoji.get(stage, '⏳')} {stage.capitalize()}")
        
        if status.get('status') == 'complete':
            st.session_state.status = 'ready'
            st.session_state.metadata = service.get_metadata(st.session_state.video_id)
            st.success("Video processed successfully!")
            time.sleep(1)
            st.rerun()
        elif status.get('status') == 'error':
            st.session_state.status = 'error'
            st.error(f"Error: {status.get('error', 'Unknown error')}")
        else:
            time.sleep(2)
            st.rerun()
    
    if st.session_state.status == 'ready' and st.session_state.metadata:
        st.divider()
        st.subheader("Video Info")
        metadata = st.session_state.metadata
        st.write(f"**Title:** {metadata.title}")
        st.write(f"**Duration:** {int(metadata.duration // 60)}:{int(metadata.duration % 60):02d}")
        st.write(f"**Chunks:** {metadata.num_chunks}")
        
        if st.button("Process New Video"):
            st.session_state.video_id = None
            st.session_state.status = 'idle'
            st.session_state.messages = []
            st.session_state.metadata = None
            st.session_state.memory.clear()
            st.rerun()

if st.session_state.status == 'ready':
    st.subheader("💬 Ask Questions")
    
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])
            
            if message['role'] == 'assistant' and message.get('sources'):
                with st.expander("📚 Sources"):
                    for i, source in enumerate(message['sources'], 1):
                        timestamp = source['timestamp_url']
                        st.markdown(f"**[{i}] Timestamp: {timestamp}**")
                        st.caption(source['text'])
                        st.divider()
    
    if question := st.chat_input("Ask a question about the video..."):
        st.session_state.messages.append({
            'role': 'user',
            'content': question
        })
        
        with st.chat_message('user'):
            st.write(question)
        
        with st.chat_message('assistant'):
            with st.spinner("Thinking..."):
                try:
                    response: RAGResponse = service.query(
                        st.session_state.video_id,
                        question,
                        use_langgraph=True
                    )
                    
                    st.write(response.answer)
                    
                    st.session_state.memory.add_turn(question, response.answer)
                    
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': response.answer,
                        'sources': response.sources
                    })
                    
                    if response.sources:
                        with st.expander("📚 Sources"):
                            for i, source in enumerate(response.sources, 1):
                                timestamp = source['timestamp_url']
                                st.markdown(f"**[{i}] Timestamp: {timestamp}**")
                                st.caption(source['text'])
                                st.divider()
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': error_msg,
                        'sources': []
                    })

elif st.session_state.status == 'idle':
    st.info("👈 Enter a YouTube URL in the sidebar to get started")
elif st.session_state.status == 'processing':
    st.info("⏳ Processing video... Please wait")
