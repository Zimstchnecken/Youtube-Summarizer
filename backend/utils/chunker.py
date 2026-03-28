"""
Transcript chunking utility — splits transcript into token-safe segments.
"""


def estimate_tokens(text: str) -> int:
    """
    Rough token estimation: ~4 characters per token for English text.
    This is a fast approximation; for exact counts use tiktoken.
    """
    return len(text) // 4


def chunk_transcript(transcript: list[dict], max_tokens: int = 6000) -> list[dict]:
    """
    Split transcript entries into token-safe chunks.
    
    Each chunk contains:
    - 'text': concatenated transcript text for the chunk
    - 'start_timestamp': timestamp of the first entry in the chunk
    - 'entries': the original transcript entries in this chunk
    
    Chunks are split at entry boundaries (never mid-sentence).
    """
    if not transcript:
        return []
    
    chunks = []
    current_chunk_entries = []
    current_chunk_text = ""
    
    for entry in transcript:
        entry_text = entry["text"]
        entry_tokens = estimate_tokens(entry_text)
        
        # If adding this entry would exceed the limit, finalize current chunk
        if (estimate_tokens(current_chunk_text) + entry_tokens > max_tokens 
                and current_chunk_entries):
            chunks.append({
                "text": current_chunk_text.strip(),
                "start_timestamp": current_chunk_entries[0]["timestamp"],
                "entries": current_chunk_entries,
            })
            current_chunk_entries = []
            current_chunk_text = ""
        
        current_chunk_entries.append(entry)
        current_chunk_text += f"[{entry['timestamp']}] {entry_text}\n"
    
    # Don't forget the last chunk
    if current_chunk_entries:
        chunks.append({
            "text": current_chunk_text.strip(),
            "start_timestamp": current_chunk_entries[0]["timestamp"],
            "entries": current_chunk_entries,
        })
    
    return chunks
