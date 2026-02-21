"""
FastAPI application for RAG chatbot
Implements /api/chat endpoint as per requirements
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List

from config import settings
from models import ChatRequest, ChatResponse, SourceChunk
from vector_store import vector_store
from openai_client import generate_embedding, generate_answer


# Initialize FastAPI app
app = FastAPI(
    title="Acme Tech Solutions RAG Chatbot",
    description="Python backend with Pinecone vector store and OpenAI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Acme Tech Solutions RAG Chatbot",
        "version": "1.0.0",
        "backend": "Python FastAPI",
        "vector_store": "Pinecone",
        "llm": settings.openai_model
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    try:
        stats = vector_store.get_stats()
        return {
            "status": "healthy",
            "pinecone_index": settings.pinecone_index_name,
            "vector_count": stats.get('total_vector_count', 0),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for RAG queries
    
    Implements Retrieval-Augmented Generation:
    1. Generate embedding for question
    2. Search Pinecone for similar chunks
    3. Build context from retrieved chunks
    4. Generate answer using GPT-3.5-turbo
    
    Args:
        request: ChatRequest with question and optional conversation history
    
    Returns:
        ChatResponse with answer and source attribution
    """
    try:
        # Validate input
        if not request.question or not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )
        
        question = request.question.strip()
        print(f"[Chat] Question: {question}")
        
        # Step 1: Generate embedding for the question
        query_embedding = generate_embedding(question)
        print(f"[Chat] Generated query embedding (dim: {len(query_embedding)})")
        
        # Step 2: Search Pinecone for similar chunks
        similar_chunks = vector_store.search(
            query_embedding=query_embedding,
            top_k=5
        )
        
        if not similar_chunks:
            return ChatResponse(
                success=False,
                error="No relevant content found in documents",
                timestamp=datetime.utcnow().isoformat()
            )
        
        print(f"[Chat] Found {len(similar_chunks)} similar chunks")
        
        # Debug: Print all scores
        for i, chunk in enumerate(similar_chunks):
            print(f"  Chunk {i+1}: score={chunk['score']:.4f}, doc={chunk['document_name']}")
        
        # Filter by similarity threshold (cosine similarity > 0.25)
        # Lowered threshold because we have full documents as single chunks
        SIMILARITY_THRESHOLD = 0.25
        relevant_chunks = [
            chunk for chunk in similar_chunks 
            if chunk['score'] >= SIMILARITY_THRESHOLD
        ]
        
        if not relevant_chunks:
            return ChatResponse(
                success=False,
                error="No sufficiently relevant content found. Try rephrasing your question.",
                timestamp=datetime.utcnow().isoformat()
            )
        
        print(f"[Chat] {len(relevant_chunks)} chunks above threshold")
        
        # Step 3: Build context from retrieved chunks
        context_parts = []
        for i, chunk in enumerate(relevant_chunks):
            context_parts.append(
                f"[Source {i + 1}: {chunk['document_name']}]\n{chunk['content']}"
            )
        
        context = "\n\n---\n\n".join(context_parts)
        
        # Step 4: Generate answer using GPT-3.5-turbo
        conversation_history = [
            {"question": msg.question, "answer": msg.answer}
            for msg in (request.conversation_history or [])
        ]
        
        answer = generate_answer(
            question=question,
            context=context,
            conversation_history=conversation_history
        )
        
        print(f"[Chat] Generated answer (length: {len(answer)})")
        
        # Step 5: Prepare sources for response
        sources = [
            SourceChunk(
                document_name=chunk['document_name'],
                chunk_text=chunk['content'],
                similarity=round(chunk['score'], 2)
            )
            for chunk in relevant_chunks
        ]
        
        return ChatResponse(
            success=True,
            answer=answer,
            sources=sources,
            timestamp=datetime.utcnow().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[Chat] Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
