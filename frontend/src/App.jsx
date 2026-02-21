import React, { useState } from 'react';
import './App.css';

const API_URL = 'http://localhost:8000/api/chat';

const DEMO_QUESTIONS = [
  "When was Acme founded?",
  "What products does Acme offer?",
  "Tell me about AcmeFlow workflow automation",
  "What is InsightEdge analytics platform?",
  "Is Acme a remote-first organization?",
  "Tell me about professional development at Acme"
];

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;

    const userQuestion = input.trim();
    setInput('');
    setLoading(true);

    // Add user message
    const userMessage = {
      role: 'user',
      content: userQuestion
    };
    setMessages(prev => [...prev, userMessage]);

    await fetchAnswer(userQuestion, messages);
  };

  const selectDemoQuestion = (question) => {
    setInput(question);
  };

  const fetchAnswer = async (userQuestion, previousMessages) => {
    try {
      // Call Python backend
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question: userQuestion,
          conversation_history: previousMessages
            .filter(m => m.role === 'user' || m.role === 'assistant')
            .slice(-6)
            .map(m => ({
              question: m.role === 'user' ? m.content : '',
              answer: m.role === 'assistant' ? m.content : ''
            }))
            .filter(m => m.question || m.answer)
        })
      });

      const data = await response.json();

      if (data.success) {
        // Add assistant message
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.answer,
          sources: data.sources || []
        }]);
      } else {
        setMessages(prev => [...prev, {
          role: 'error',
          content: data.error || 'An error occurred'
        }]);
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        role: 'error',
        content: 'Failed to connect to server. Make sure the Python backend is running on port 8000.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>💬 Acme Tech Solutions</h1>
        <p>Ask me anything about Acme Tech Solutions</p>
      </div>

          <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h2>👋 Welcome to Acme Tech Solutions!</h2>
            <p>Ask me anything about our company</p>
            
            <div className="demo-questions">
              <p className="demo-label">💡 Try these questions:</p>
              <div className="demo-buttons">
                {DEMO_QUESTIONS.map((question, idx) => (
                  <button
                    key={idx}
                    className="demo-btn"
                    onClick={() => selectDemoQuestion(question)}
                    disabled={loading}
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-content">
                {message.content}
                {message.sources && message.sources.length > 0 && (
                  <div className="sources">
                    <strong>Sources:</strong>
                    {message.sources.map((source, idx) => (
                      <div key={idx} className="source-item">
                        📄 {source.document_name} (similarity: {(source.similarity * 100).toFixed(0)}%)
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="message assistant loading">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
      </div>

      <form className="chat-input" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question here..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}

export default App;
