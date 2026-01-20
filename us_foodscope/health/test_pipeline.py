import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_service import RAGService

def test_rag():
    print("--- Testing RAG Pipeline ---")
    
    # Initialize Service
    service = RAGService()
    try:
        service.initialize()
    except Exception as e:
        print(f"FAILED: Initialization error: {e}")
        return

    if not service.initialized:
        print("FAILED: Service not initialized.")
        return

    # Test Retrieval
    query = "What is the obesity rate in counties with high risk?"
    print(f"Testing retrieval for query: '{query}'")
    
    try:
        results = service.retrieve(query, top_k=3)
        if not results:
            print("FAILED: No results retrieved.")
            return
        
        print(f"SUCCESS: Retrieved {len(results)} chunks.")
        for i, (chunk, score) in enumerate(results):
            print(f"Chunk {i+1} [Score: {score:.4f}]: {chunk.text[:100]}...")
            
    except Exception as e:
        print(f"FAILED: Retrieval error: {e}")
        return

    # Check for Groq API Key and test generation
    if os.environ.get("GROQ_API_KEY"):
        print("INFO: GROQ_API_KEY found. Testing full RAG generation...")
        try:
            result = service.ask(query)
            if "error" in result:
                print(f"FAILED: Generation error: {result['error']}")
            else:
                print("SUCCESS: Full RAG answer generated!")
                print(f"Answer: {result['answer'][:200]}...")
        except Exception as e:
            print(f"FAILED: Generation exception: {e}")
    else:
        print("INFO: GROQ_API_KEY not found. Skipping 'ask' generation test.")

    print("--- Pipeline Check Complete ---")

if __name__ == "__main__":
    test_rag()
