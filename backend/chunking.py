"""
Text chunking utilities for document processing
Implements 512-word chunking as per requirements
"""

from typing import List, Dict


def count_words(text: str) -> int:
    """Count words in text"""
    return len(text.strip().split())


def chunk_text_by_words(text: str, words_per_chunk: int = 512) -> List[Dict[str, any]]:
    """
    Split text into chunks by word count
    
    Args:
        text: The text to chunk
        words_per_chunk: Number of words per chunk (default: 512)
    
    Returns:
        List of chunks with content and metadata
    """
    words = text.strip().split()
    chunks = []
    
    for i in range(0, len(words), words_per_chunk):
        chunk_words = words[i:i + words_per_chunk]
        content = ' '.join(chunk_words)
        
        chunks.append({
            'content': content,
            'word_count': len(chunk_words),
            'chunk_index': i // words_per_chunk
        })
    
    return chunks


def chunk_text_by_paragraphs(text: str, max_words: int = 512) -> List[Dict[str, any]]:
    """
    Split text into chunks by paragraphs, respecting word limit
    
    Args:
        text: The text to chunk
        max_words: Maximum words per chunk
    
    Returns:
        List of chunks with content and metadata
    """
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    current_chunk = []
    current_word_count = 0
    chunk_index = 0
    
    for paragraph in paragraphs:
        para_words = count_words(paragraph)
        
        # If adding this paragraph exceeds limit, finalize current chunk
        if current_word_count + para_words > max_words and current_chunk:
            content = '\n\n'.join(current_chunk)
            chunks.append({
                'content': content,
                'word_count': current_word_count,
                'chunk_index': chunk_index
            })
            current_chunk = []
            current_word_count = 0
            chunk_index += 1
        
        current_chunk.append(paragraph)
        current_word_count += para_words
    
    # Add remaining chunk
    if current_chunk:
        content = '\n\n'.join(current_chunk)
        chunks.append({
            'content': content,
            'word_count': current_word_count,
            'chunk_index': chunk_index
        })
    
    return chunks
