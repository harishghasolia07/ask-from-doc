"""
Load Acme Tech Solutions documents into Pinecone
Run this script to initialize the knowledge base
"""

import os
import sys
from pathlib import Path

from chunking import chunk_text_by_words
from openai_client import generate_batch_embeddings
from vector_store import vector_store
from config import settings


# Documents directory (relative to backend directory)
DOCUMENTS_DIR = Path(__file__).parent.parent / "documents"

ACME_DOCUMENTS = [
    "company_history.txt",
    "core_products.txt",
    "hr_policy.txt"
]


def load_documents():
    """Load all Acme Tech Solutions documents into Pinecone"""
    
    print("=" * 60)
    print("Loading Acme Tech Solutions Documents into Pinecone")
    print("=" * 60)
    print()
    
    total_chunks = 0
    
    for filename in ACME_DOCUMENTS:
        filepath = DOCUMENTS_DIR / filename
        
        print(f"📄 Processing: {filename}")
        
        if not filepath.exists():
            print(f"   ⚠️  File not found: {filepath}")
            print(f"   Skipping...")
            print()
            continue
        
        # Read file content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            print(f"   ⚠️  File is empty")
            print(f"   Skipping...")
            print()
            continue
        
        print(f"   📖 Read {len(content)} characters")
        
        # Chunk the text using 512-word chunks
        chunks = chunk_text_by_words(content, words_per_chunk=settings.chunk_size)
        print(f"   ✂️  Created {len(chunks)} chunks")
        
        # Generate embeddings for all chunks
        chunk_texts = [chunk['content'] for chunk in chunks]
        print(f"   🔢 Generating embeddings...")
        embeddings = generate_batch_embeddings(chunk_texts)
        print(f"   ✅ Generated {len(embeddings)} embeddings")
        
        # Store in Pinecone
        print(f"   💾 Storing in Pinecone...")
        num_stored = vector_store.upsert_chunks(
            chunks=chunks,
            embeddings=embeddings,
            document_name=filename
        )
        print(f"   ✅ Stored {num_stored} chunks")
        print()
        
        total_chunks += num_stored
    
    print("=" * 60)
    print(f"✨ Loading complete! Total chunks stored: {total_chunks}")
    print("=" * 60)
    
    # Show index stats
    try:
        stats = vector_store.get_stats()
        print()
        print("Pinecone Index Stats:")
        print(f"  - Index: {settings.pinecone_index_name}")
        print(f"  - Total vectors: {stats.get('total_vector_count', 0)}")
        print(f"  - Dimension: {settings.embedding_dimension}")
        print()
    except Exception as e:
        print(f"Could not fetch stats: {e}")


if __name__ == "__main__":
    try:
        load_documents()
        print("✅ Success! Documents are ready for querying.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
