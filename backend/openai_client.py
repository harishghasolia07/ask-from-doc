"""
OpenAI integration for embeddings and LLM
"""

from typing import List
from openai import OpenAI
from config import settings


# Initialize OpenAI client
client = OpenAI(api_key=settings.openai_api_key)


def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text
    
    Args:
        text: Text to embed
    
    Returns:
        Embedding vector
    """
    response = client.embeddings.create(
        model=settings.embedding_model,
        input=text
    )
    return response.data[0].embedding


def generate_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts
    
    Args:
        texts: List of texts to embed
    
    Returns:
        List of embedding vectors
    """
    response = client.embeddings.create(
        model=settings.embedding_model,
        input=texts
    )
    return [item.embedding for item in response.data]


def generate_answer(
    question: str,
    context: str,
    conversation_history: List[dict] = None
) -> str:
    """
    Generate answer using GPT-3.5-turbo
    
    Args:
        question: User's question
        context: Retrieved context from documents
        conversation_history: Previous messages for context
    
    Returns:
        Generated answer
    """
    system_prompt = """You are a helpful assistant that answers questions based ONLY on the provided context from documents.

IMPORTANT RULES:
1. Answer ONLY using information from the provided context
2. If the answer is not found in the context, respond with "Not found in documents."
3. Cite which document(s) you used to answer the question
4. Be concise and accurate
5. Do not make up information or use external knowledge
6. Use conversation history to understand follow-up questions and references"""

    # Build conversation context
    messages = [{"role": "system", "content": system_prompt}]
    
    if conversation_history:
        for msg in conversation_history[-3:]:  # Last 3 messages
            messages.append({"role": "user", "content": msg.get("question", "")})
            messages.append({"role": "assistant", "content": msg.get("answer", "")})
    
    # Add current question with context
    user_prompt = f"""Context from documents:

{context}

---

Current Question: {question}

Please answer the current question based on the context above."""
    
    messages.append({"role": "user", "content": user_prompt})
    
    # Call OpenAI
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        temperature=0.3,
        max_tokens=1000
    )
    
    return response.choices[0].message.content
