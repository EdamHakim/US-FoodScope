import os
import pandas as pd
import numpy as np
import faiss
import pickle
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from groq import Groq
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

@dataclass
class Chunk:
    text: str
    metadata: Dict[str, Any]
    chunk_id: int

class RAGService:
    def __init__(self, 
                 csv_path: str = "rag_df.csv", 
                 index_path: str = "faiss_index.bin", 
                 chunks_path: str = "chunks.pkl",
                 model_name: str = "all-MiniLM-L6-v2"):
        self.csv_path = csv_path
        self.index_path = index_path
        self.chunks_path = chunks_path
        self.model_name = model_name
        self.model = None
        self.index = None
        self.chunks = []
        self.client = None
        self.initialized = False

    def initialize(self):
        """Initialize models and indices"""
        if self.initialized:
            return

        # Load Embedding Model
        print(f"Loading embedding model: {self.model_name}...")
        self.model = SentenceTransformer(self.model_name)

        # Load FAISS Index
        if os.path.exists(self.index_path):
            print(f"Loading FAISS index from {self.index_path}...")
            self.index = faiss.read_index(self.index_path)
        else:
            print(f"Warning: {self.index_path} not found. RAG will not work.")

        # Load Chunks
        if os.path.exists(self.chunks_path):
            print(f"Loading chunks from {self.chunks_path}...")
            with open(self.chunks_path, 'rb') as f:
                self.chunks = pickle.load(f)
        else:
            print(f"Warning: {self.chunks_path} not found.")

        # Initialize Groq Client
        api_key = os.environ.get("GROQ_API_KEY")
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            print("Warning: GROQ_API_KEY not found in environment.")

        self.initialized = True

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Chunk, float]]:
        if not self.index or not self.chunks:
            return []

        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if 0 <= idx < len(self.chunks):
                # For normalized vectors, dist from index.search is:
                # 1. Cosine similarity if using IndexFlatIP
                # 2. Squared L2 distance if using IndexFlatL2 (dist = 2 - 2*sim)
                # We'll assume Inner Product (Similarity) for now, but cap it [0,1]
                similarity = max(0.0, min(1.0, float(dist)))
                results.append((self.chunks[idx], similarity))
        
        return results

    def ask(self, query: str) -> Dict[str, Any]:
        if not self.initialized:
            self.initialize()

        if not self.client:
            return {"error": "Groq client not initialized. Set GROQ_API_KEY environment variable."}

        # Retrieve (Increased to 10 for better data coverage)
        relevant_chunks = self.retrieve(query, top_k=10)
        context = "\n\n".join([f"[Source: {c.metadata.get('county', 'Unknown')}, {c.metadata.get('state', 'Unknown')}] {c.text}" for c, _ in relevant_chunks])

        # Generate
        prompt = f"""
        You are an expert in U.S. food environment and health analysis. 
        Use the following retrieved context to answer the user's question accurately.
        
        FORMATTING & STYLE RULES:
        1. NEVER mention words like "context", "provided data", "the text above", or "based on the information" in your response.
        2. Speak directly as an expert performing the analysis.
        3. Use **bold text** for key metrics like percentages or scores.
        4. Use bullet points for lists of facts or recommendations.
        5. Use Markdown TABLES when comparing data for two or more counties.
        6. Keep your tone professional, authoritative, and data-driven.
        
        Context:
        {context}
        
        User Question: {query}
        
        Answer:
        """

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=1024,
            )
            response_text = completion.choices[0].message.content
            
            # Prepare sources with similarity scores
            sources = []
            for c, score in relevant_chunks:
                source_info = c.metadata.copy()
                source_info["similarity"] = score
                sources.append(source_info)
            
            return {
                "answer": response_text,
                "sources": sources,
                "context_used": context
            }
        except Exception as e:
            return {"error": str(e)}
