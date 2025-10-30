import faiss
import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer
from datetime import datetime

class VectorStore:
    def __init__(self, embedding_model='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(embedding_model)
        self.embedding_dim = 384
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        self.metadata = []
        
    def add_conversation(self, user_id: str, session_id: str, user_message: str, 
                        agent_response: str, agent_used: str):
        text = f"User: {user_message} Agent: {agent_response}"
        embedding = self.model.encode([text])[0]
        
        self.index.add(embedding.astype('float32').reshape(1, -1))
        
        metadata = {
            'user_id': user_id,
            'session_id': session_id,
            'user_message': user_message,
            'agent_response': agent_response,
            'agent_used': agent_used,
            'timestamp': datetime.now().isoformat()
        }
        self.metadata.append(metadata)