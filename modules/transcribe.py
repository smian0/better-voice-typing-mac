import os
import torch
import whisper
import tiktoken
import wave
from typing import Optional, Dict, Any, NamedTuple
from functools import lru_cache

# Track session totals
session_tokens_sent = 0
session_tokens_received = 0
session_cost = 0.0

class TranscriptionResult(NamedTuple):
    text: str
    tokens_sent: int    # Audio duration in tokens (roughly 1 second = 50 tokens)
    tokens_received: int  # Output text tokens
    message_cost: float  # Cost of this message
    session_cost: float  # Total session cost

@lru_cache(maxsize=1)
def load_whisper_model(model_name: str = "base") -> Any:
    """Load and cache the Whisper model with proper settings to avoid warnings"""
    # Monkey patch torch.load to use weights_only=True
    original_load = torch.load
    def safe_load(*args, **kwargs):
        kwargs['weights_only'] = True
        return original_load(*args, **kwargs)
    torch.load = safe_load
    
    try:
        model = whisper.load_model(model_name, device="cpu")
        return model
    finally:
        # Restore original torch.load
        torch.load = original_load

def count_tokens(text: str) -> int:
    """Count tokens in text using GPT tokenizer"""
    encoder = tiktoken.get_encoding("cl100k_base")  # Same encoding used by Whisper
    return len(encoder.encode(text))

def get_audio_duration(audio_file: str) -> float:
    """Get duration of audio file in seconds"""
    with wave.open(audio_file, 'rb') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        return duration

def calculate_cost(duration_seconds: float) -> float:
    """Calculate cost in USD based on Whisper API pricing"""
    # Current Whisper API pricing: $0.006 per minute
    cost_per_minute = 0.006
    duration_minutes = duration_seconds / 60
    return duration_minutes * cost_per_minute

def transcribe_audio(audio_file: str) -> TranscriptionResult:
    """
    Transcribe audio file using Whisper
    Returns: TranscriptionResult with text, token count, duration, and cost
    """
    global session_tokens_sent, session_tokens_received, session_cost
    
    model = load_whisper_model("base")
    result = model.transcribe(
        audio_file,
        fp16=False  # Explicitly disable FP16 to avoid warnings
    )
    text = result["text"].strip()
    
    # Calculate tokens and costs
    duration = get_audio_duration(audio_file)
    tokens_sent = int(duration * 50)  # Approximate tokens per second of audio
    tokens_received = count_tokens(text)
    message_cost = calculate_cost(duration)
    
    # Update session totals
    session_tokens_sent += tokens_sent
    session_tokens_received += tokens_received
    session_cost += message_cost
    
    print(f"Tokens: {tokens_sent} sent, {tokens_received} received. Cost: ${message_cost:.4f} message, ${session_cost:.4f} session")
    
    return TranscriptionResult(
        text=text,
        tokens_sent=session_tokens_sent,  # Return session totals
        tokens_received=session_tokens_received,  # Return session totals
        message_cost=message_cost,
        session_cost=session_cost
    )

def reset_session_stats() -> None:
    """Reset session statistics"""
    global session_cost, session_tokens_sent, session_tokens_received
    session_cost = 0.0
    session_tokens_sent = 0
    session_tokens_received = 0