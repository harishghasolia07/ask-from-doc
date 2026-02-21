# Python Backend - RAG Chatbot

This is the **Python FastAPI backend** implementation that fulfills the exact requirements from `Requirements.md`:

- ✅ **Python** backend (FastAPI)
- ✅ **Pinecone** vector database
- ✅ **OpenAI** embeddings and gpt-3.5-turbo
- ✅ **512-word chunking**
- ✅ **/api/chat** REST endpoint
- ✅ **3 Acme Tech Solutions documents**

## Architecture

```
backend/
├── main.py              # FastAPI app with /api/chat endpoint
├── config.py            # Configuration from environment variables
├── models.py            # Pydantic models for request/response
├── vector_store.py      # Pinecone integration
├── openai_client.py     # OpenAI embeddings + LLM
├── chunking.py          # 512-word text chunking
├── load_documents.py    # Script to load Acme documents
├── test_chat.py         # Test script
├── requirements.txt     # Python dependencies
└── .env.example         # Environment variables template
```

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- Pinecone account (free tier): https://www.pinecone.io/
- OpenAI API key: https://platform.openai.com/

### 2. Create Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

Required variables:
```env
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=pcsk_...
PINECONE_ENVIRONMENT=gcp-starter  # or your Pinecone environment
PINECONE_INDEX_NAME=acme-docs
```

### 5. Load Acme Documents

```bash
# This will create the Pinecone index and load the 3 documents
python load_documents.py
```

Expected output:
```
================================================================
Loading Acme Tech Solutions Documents into Pinecone
================================================================

📄 Processing: company_history.txt
   📖 Read 1729 characters
   ✂️  Created 1 chunks
   🔢 Generating embeddings...
   ✅ Generated 1 embeddings
   💾 Storing in Pinecone...
   ✅ Stored 1 chunks

...

✨ Loading complete! Total chunks stored: 3
```

### 6. Run the Server

```bash
# Development mode with auto-reload
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start on: http://localhost:8000

### 7. Test the API

#### Health Check

```bash
curl http://localhost:8000/health
```

#### Chat Endpoint

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "When was Acme Tech Solutions founded?",
    "conversation_history": []
  }'
```

Expected response:
```json
{
  "success": true,
  "answer": "Acme Tech Solutions was founded in 2015...",
  "sources": [
    {
      "document_name": "company_history.txt",
      "chunk_text": "...",
      "similarity": 0.89
    }
  ],
  "timestamp": "2026-02-20T..."
}
```

## API Documentation

### POST /api/chat

Main endpoint for RAG queries.

**Request Body:**
```json
{
  "question": "Your question here",
  "conversation_history": [
    {
      "question": "Previous question",
      "answer": "Previous answer"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "answer": "Generated answer based on documents",
  "sources": [
    {
      "document_name": "company_history.txt",
      "chunk_text": "Relevant text chunk",
      "similarity": 0.85
    }
  ],
  "timestamp": "2026-02-20T10:30:00.000Z"
}
```

### GET /

Health check endpoint.

### GET /health

Detailed health check with Pinecone stats.

## Interactive API Documentation

FastAPI automatically generates interactive API docs:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Testing

Run the test script:

```bash
python test_chat.py
```

This will ask several questions about Acme Tech Solutions and display the answers.

## Connecting Next.js Frontend

To use this Python backend with the existing Next.js frontend:

1. **Update Next.js to call Python backend:**

```typescript
// In your Next.js API route or component
const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: userQuestion,
    conversation_history: []
  })
});

const data = await response.json();
```

2. **Update CORS in backend if needed:**

Edit `backend/.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## RAG Pipeline

The `/api/chat` endpoint implements a complete RAG pipeline:

1. **Embed Query** - Convert user question to vector using OpenAI embeddings
2. **Search** - Find similar chunks in Pinecone using cosine similarity
3. **Filter** - Keep only chunks with similarity > 0.7
4. **Build Context** - Combine retrieved chunks into context string
5. **Generate** - Use GPT-3.5-turbo with context to generate answer
6. **Return** - Send answer with source attribution

## Tech Stack (Requirements-Compliant)

| Component | Technology |
|-----------|-----------|
| Language | Python 3.9+ |
| Framework | FastAPI |
| Vector DB | Pinecone (cloud) |
| Embeddings | OpenAI text-embedding-3-small |
| LLM | OpenAI gpt-3.5-turbo |
| Chunking | 512-word chunks |
| API | REST endpoint at /api/chat |

## Project Structure

```
backend/
├── main.py              # FastAPI application
│   └── /api/chat        # Main chat endpoint
├── config.py            # Settings management
├── models.py            # Pydantic models
├── vector_store.py      # Pinecone operations
├── openai_client.py     # OpenAI API calls
├── chunking.py          # Text processing
├── load_documents.py    # Data loading script
├── test_chat.py         # Testing utilities
├── requirements.txt     # Dependencies
├── .env                 # Environment variables (not in git)
└── .env.example         # Template
```

## Troubleshooting

### Pinecone connection errors

Make sure:
- API key is correct
- Environment matches your Pinecone project (e.g., `gcp-starter`, `us-east-1-aws`)
- Index name doesn't conflict with existing indexes

### OpenAI rate limits

Free tier has rate limits. If you hit them:
- Add delays between requests
- Upgrade to paid tier
- Use smaller batch sizes in `load_documents.py`

### No relevant content found

If queries return "No relevant content found":
- Check that documents were loaded: `python load_documents.py`
- Lower similarity threshold in `main.py` (line 89)
- Verify Pinecone index has vectors: Check `/health` endpoint

## Development

### Add new documents

1. Place `.txt` files in `../documents/`
2. Add filenames to `ACME_DOCUMENTS` in `load_documents.py`
3. Run `python load_documents.py` again

### Change chunking strategy

Edit `chunking.py` or adjust `CHUNK_SIZE` in `.env`

### Switch LLM model

Edit `.env`:
```env
OPENAI_MODEL=gpt-4  # or gpt-4-turbo, etc.
```

## Deployment

For production deployment:

1. **Railway / Render / Heroku:**
   - Add `Procfile`: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Set environment variables in dashboard

2. **Docker:**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

3. **AWS Lambda:**
   - Use Mangum adapter for FastAPI on Lambda
   - Store Pinecone API keys in AWS Secrets Manager

## License

This backend implementation is part of the Distinct Cloud Labs assignment submission.
