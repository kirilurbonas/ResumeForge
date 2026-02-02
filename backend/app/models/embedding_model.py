"""Embedding model wrapper."""

from sentence_transformers import SentenceTransformer
import os


class EmbeddingModel:
    """Wrapper for sentence transformer embedding model."""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the embedding model."""
        try:
            self.model = SentenceTransformer(self.model_name)
        except Exception as e:
            raise ValueError(f"Failed to load embedding model {self.model_name}: {str(e)}")
    
    def encode(self, texts: list) -> list:
        """Encode texts to embeddings."""
        if not self.model:
            self._load_model()
        return self.model.encode(texts, convert_to_numpy=True).tolist()
    
    def encode_single(self, text: str) -> list:
        """Encode a single text to embedding."""
        return self.encode([text])[0]
