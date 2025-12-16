"""Audio transcription using faster-whisper."""
from faster_whisper import WhisperModel
from typing import List
from backend.models import TranscriptSegment

class Transcriber:
    """Transcribes audio files with timestamp preservation."""
    
    def __init__(self, model_size: str = "base", device: str = "cpu"):
        """
        Initialize Whisper model.
        
        Args:
            model_size: tiny, base, small, medium, large-v2
            device: cpu or cuda
        """
        self.model = WhisperModel(model_size, device=device, compute_type="int8")
    
    def transcribe(self, audio_path: str) -> List[TranscriptSegment]:
        """
        Transcribe audio file with word-level timestamps.
        
        Returns:
            List of TranscriptSegment with text and timestamps
        """
        segments, info = self.model.transcribe(
            audio_path,
            beam_size=5,
            word_timestamps=True,
            vad_filter=True,  # Voice activity detection
        )
        
        transcript_segments = []
        for segment in segments:
            transcript_segments.append(TranscriptSegment(
                text=segment.text.strip(),
                start=segment.start,
                end=segment.end
            ))
        
        return transcript_segments
