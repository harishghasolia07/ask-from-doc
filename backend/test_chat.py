"""
Test the RAG chatbot functionality
"""

import asyncio
from main import chat
from models import ChatRequest, ChatMessage


async def test_chat():
    """Test the chat endpoint with sample questions"""
    
    print("=" * 60)
    print("Testing Acme Tech Solutions RAG Chatbot")
    print("=" * 60)
    print()
    
    # Test questions about Acme Tech Solutions
    questions = [
        "When was Acme Tech Solutions founded?",
        "What products does Acme Tech offer?",
        "What is AcmeFlow?",
        "What are the HR policies at Acme?",
    ]
    
    conversation_history = []
    
    for i, question in enumerate(questions, 1):
        print(f"Question {i}: {question}")
        print("-" * 60)
        
        request = ChatRequest(
            question=question,
            conversation_history=conversation_history
        )
        
        try:
            response = await chat(request)
            
            if response.success:
                print(f"Answer: {response.answer}")
                print()
                print(f"Sources ({len(response.sources)}):")
                for j, source in enumerate(response.sources, 1):
                    print(f"  {j}. {source.document_name} (similarity: {source.similarity})")
                print()
                
                # Add to conversation history
                conversation_history.append(
                    ChatMessage(question=question, answer=response.answer)
                )
            else:
                print(f"Error: {response.error}")
                print()
        
        except Exception as e:
            print(f"Error: {e}")
            print()
        
        print("=" * 60)
        print()


if __name__ == "__main__":
    print("Make sure you have:")
    print("1. Loaded documents using: python load_documents.py")
    print("2. Set OPENAI_API_KEY and PINECONE_API_KEY in .env")
    print()
    input("Press Enter to continue...")
    print()
    
    asyncio.run(test_chat())
