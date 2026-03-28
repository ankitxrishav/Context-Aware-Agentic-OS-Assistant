import os
import chromadb
import ollama
from typing import List, Dict, Any, Optional
from datetime import datetime

class MemoryManager:
    def __init__(self, db_path: str = "./memory_db", model: str = "nomic-embed-text"):
        self.db_path = db_path
        self.model = model
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection(name="agent_memory")
        self.ollama_client = ollama.Client()

    def _get_embedding(self, text: str) -> List[float]:
        """Generates an embedding for the given text using Ollama."""
        response = self.ollama_client.embed(model=self.model, input=text)
        return response.get("embeddings", [[]])[0]

    def add_memory(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        """Adds a new memory to the vector database."""
        if not metadata:
            metadata = {}
        
        metadata["timestamp"] = datetime.now().isoformat()
        embedding = self._get_embedding(text)
        
        # Use a simple counter or timestamp as ID
        memory_id = f"mem_{int(datetime.now().timestamp() * 1000)}"
        
        self.collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata]
        )
        print(f"-- Stored memory: '{text[:50]}...'")

    def query_memory(self, query: str, n_results: int = 3) -> str:
        """Retrieves the most relevant memories for a given query."""
        try:
            query_embedding = self._get_embedding(query)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            documents = results.get("documents", [[]])[0]
            if not documents:
                return ""
            
            context = "\n".join([f"- {doc}" for doc in documents])
            return context
        except Exception as e:
            print(f"Memory: Error querying database: {str(e)}")
            return ""
