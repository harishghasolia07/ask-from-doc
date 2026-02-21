# React Frontend for Acme Tech Solutions RAG Chatbot

Simple React frontend that connects to the Python FastAPI backend.

## Features

- ✅ Clean, modern chat interface
- ✅ Input box for user questions
- ✅ Send button
- ✅ Conversation history display
- ✅ Source attribution display
- ✅ Loading states
- ✅ Error handling
- ✅ Responsive design

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Vanilla CSS** - Styling

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

Make sure your Python backend is running on port 8000, then:

```bash
npm run dev
```

Frontend will run on: http://localhost:3001

## Usage

1. **Make sure Python backend is running:**
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```

2. **Start frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open browser:** http://localhost:3001

4. **Ask questions:**
   - "When was Acme Tech Solutions founded?"
   - "What products does Acme offer?"
   - "What are the HR policies?"

## Project Structure

```
frontend/
├── index.html          # HTML entry point
├── package.json        # Dependencies
├── vite.config.js      # Vite configuration
├── src/
│   ├── main.jsx       # React entry point
│   ├── App.jsx        # Main chat component
│   ├── App.css        # Chat interface styles
│   └── index.css      # Global styles
└── README.md          # This file
```

## API Integration

The frontend calls the Python backend at `http://localhost:8000/api/chat`:

```javascript
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: "Your question",
    conversation_history: []
  })
})
```

## Building for Production

```bash
npm run build
```

This creates a `dist/` folder with static files that can be deployed anywhere.

## Troubleshooting

### "Failed to connect to server"

- Make sure Python backend is running on port 8000
- Check `python main.py` in backend directory
- Verify http://localhost:8000/health returns a response

### Port 3001 already in use

Change port in `vite.config.js`:
```javascript
server: {
  port: 3002,  // or any other port
  ...
}
```

### CORS errors

CORS is already configured in the Python backend to allow `localhost:3001`.
If using a different port, update `backend/.env`:
```env
CORS_ORIGINS=http://localhost:3001,http://localhost:YOUR_PORT
```

## Requirements Compliance

This frontend fulfills the requirements:

✅ **Framework:** React (as specified)  
✅ **Clean, modern chat interface**  
✅ **Input box** for user queries  
✅ **Send button**  
✅ **Conversation history** display  
✅ **Calls backend** `/api/chat` endpoint  
✅ **Updates UI** with responses  

## Features

- Real-time chat interface
- Source attribution with similarity scores
- Loading indicators
- Error handling and display
- Responsive mobile design
- Smooth animations
- Beautiful gradient design
