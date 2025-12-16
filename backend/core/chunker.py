"""Transcript chunking with timestamp preservation."""
from typing import List
from backend.models import TranscriptSegment, DocumentChunk
import tiktoken

class TranscriptChunker:
    """Chunks transcript segments while preserving timestamps."""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        """
        Args:
            chunk_size: Target tokens per chunk
            overlap: Overlapping tokens between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def chunk(self, segments: List[TranscriptSegment], video_id: str) -> List[DocumentChunk]:
        """
        Chunk transcript segments into overlapping chunks.
        
        Strategy:
        - Accumulate segments until chunk_size is reached
        - Preserve segment boundaries (don't split mid-sentence)
        - Track start_time of first segment and end_time of last segment
        - Create overlap by including last N tokens from previous chunk
        """
        chunks = []
        current_text = []
        current_segments = []
        current_tokens = 0
        chunk_index = 0
        
        for segment in segments:
            segment_tokens = len(self.tokenizer.encode(segment.text))
            
            # If adding this segment exceeds chunk_size, finalize current chunk
            if current_tokens + segment_tokens > self.chunk_size and current_segments:
                chunk = self._create_chunk(
                    current_segments, 
                    video_id, 
                    chunk_index
                )
                chunks.append(chunk)
                chunk_index += 1
                
                # Create overlap: keep last segments that fit in overlap size
                overlap_segments = self._get_overlap_segments(current_segments)
                current_segments = overlap_segments
                current_tokens = sum(
                    len(self.tokenizer.encode(s.text)) for s in current_segments
                )
            
            current_segments.append(segment)
            current_tokens += segment_tokens
        
        # Add final chunk
        if current_segments:
            chunk = self._create_chunk(current_segments, video_id, chunk_index)
            chunks.append(chunk)
        
        return chunks
    
    def _create_chunk(
        self, 
        segments: List[TranscriptSegment], 
        video_id: str, 
        index: int
    ) -> DocumentChunk:
        """Create a DocumentChunk from segments."""
        text = " ".join(s.text for s in segments)
        start_time = segments[0].start
        end_time = segments[-1].end
        chunk_id = f"{video_id}_chunk_{index}"
        
        return DocumentChunk(
            chunk_id=chunk_id,
            video_id=video_id,
            text=text,
            start_time=start_time,
            end_time=end_time,
            chunk_index=index
        )
    
    def _get_overlap_segments(self, segments: List[TranscriptSegment]) -> List[TranscriptSegment]:
        """Get last N segments that fit within overlap token limit."""
        overlap_segments = []
        overlap_tokens = 0
        
        for segment in reversed(segments):
            segment_tokens = len(self.tokenizer.encode(segment.text))
            if overlap_tokens + segment_tokens > self.overlap:
                break
            overlap_segments.insert(0, segment)
            overlap_tokens += segment_tokens
        
        return overlap_segments
