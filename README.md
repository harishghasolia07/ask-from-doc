# Acme Tech Solutions - RAG Chatbot

A basic RAG (Retrieval-Augmented Generation) chatbot application that allows users to ask questions about Acme Tech Solutions using AI-powered semantic search.

This implementation follows the specifications in [Requirements.md](./Requirements.md).

## Features

- 💬 **Simple Chat Interface**: Clean, modern interface for asking questions
- 🔍 **Semantic Search**: Find relevant information using vector similarity search (Pinecone)
- 🤖 **AI-Powered Answers**: Get accurate answers using OpenAI GPT-3.5-turbo
- 📊 **Source Attribution**: See which documents and chunks were used for each answer
- 📚 **Pre-loaded Documents**: Three Acme Tech Solutions documents already loaded

## Tech Stack

### Backend ([backend/](./backend/))
- **Python 3.11+** with FastAPI
- **Pinecone** for vector database (cloud-hosted)
- **OpenAI API** for embeddings (text-embedding-3-small) and generation (gpt-3.5-turbo)
- **512-word chunking** as per requirements

### Frontend ([frontend/](./frontend/))
- **React 18** with modern hooks
- **Vite** for fast development and building
- **Vanilla CSS** for styling

### Documents ([backend/documents/](./backend/documents/))
- **Company History** - Founding and growth since 2015
- **Core Products** - AcmeFlow, InsightEdge, SupportBot
- **HR Policy** - Remote work policies and benefits

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys:
# - OPENAI_API_KEY
# - PINECONE_API_KEY
```

### 2. Load Documents

```bash
# From backend/ directory
python load_documents.py
```

This loads the 3 Acme documents into Pinecone (only needs to be done once).

### 3. Start Backend Server

```bash
# From backend/ directory
python main.py
```

Server runs on http://localhost:8000

### 4. Frontend Setup

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on http://localhost:3001

### 5. Use the Chatbot

Open http://localhost:3001 in your browser and start asking questions!

**Example questions:**
- "When was Acme Tech Solutions founded?"
- "What products does Acme offer?"
- "What is the remote work policy?"

## Project Structure

```
.
├── backend/                 # Python FastAPI backend
│   ├── documents/          # Acme Tech Solutions text files
│   ├── main.py            # FastAPI application
│   ├── config.py          # Configuration management
│   ├── models.py          # Pydantic models
│   ├── vector_store.py    # Pinecone integration
│   ├── openai_client.py   # OpenAI API calls
│   ├── chunking.py        # Text chunking logic
│   ├── load_documents.py  # Document loader script
│   └── requirements.txt   # Python dependencies
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx       # Main chat component
│   │   ├── App.css       # Styling
│   │   └── main.jsx      # Entry point
│   ├── package.json      # npm dependencies
│   └── vite.config.js    # Vite configuration
│
├── README.md              # This file
└── Requirements.md        # Original project requirements
```

## API Endpoints

### Backend (http://localhost:8000)

- **GET /** - Health check
- **GET /health** - Detailed health status with Pinecone stats
- **POST /api/chat** - Chat endpoint
  ```json
  {
    "question": "When was Acme founded?",
    "conversation_history": []
  }
  ```

## Environment Variables

### Backend (.env)
```bash
OPENAI_API_KEY=sk-...           # Get from OpenAI
PINECONE_API_KEY=...            # Get from Pinecone
PINECONE_ENVIRONMENT=gcp-starter
PINECONE_INDEX_NAME=acme-docs
```

## Requirements Compliance

This implementation fulfills all requirements from [Requirements.md](./Requirements.md):

✅ **Data Source**: 3 text files (200+ words each) about Acme Tech Solutions  
✅ **Chunking**: 512-word text chunking  
✅ **Backend**: Python with FastAPI  
✅ **Vector Store**: Pinecone (free tier)  
✅ **Embeddings**: OpenAI text-embedding-3-small  
✅ **LLM**: OpenAI gpt-3.5-turbo  
✅ **API Endpoint**: /api/chat  
✅ **Frontend**: React with modern chat interface  
✅ **Features**: Input box, send button, conversation history  

## Troubleshooting

**Backend won't start:**
- Ensure Python 3.11+ is installed
- Activate virtual environment: `source venv/bin/activate`
- Check `.env` file has valid API keys

**Frontend won't connect:**
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify CORS is enabled (configured in main.py)

**No results from queries:**
- Confirm documents are loaded: `python load_documents.py`
- Check Pinecone dashboard to verify index exists
- Review backend logs for errors

## License

MIT
# ask-from-doc
