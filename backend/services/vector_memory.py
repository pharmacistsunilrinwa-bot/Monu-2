import chromadb
import logging

class VectorMemoryService:
    def __init__(self, path="/data/data/com.termux/files/home/.monu_vector_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name="monu_memory")
        self.logger = logging.getLogger("VectorMemoryService")

    def add_document(self, doc_id, document, metadata=None):
        self.collection.add(
            documents=[document],
            metadatas=[metadata] if metadata else None,
            ids=[doc_id]
        )
        self.logger.info(f"Added to vector memory: {doc_id}")

    def query(self, query_text, n_results=2):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results
