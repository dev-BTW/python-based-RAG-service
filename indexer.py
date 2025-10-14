import json
import faiss
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

class Indexer:
    def __init__(self, chunk_size=500, chunk_overlap=50, embedding_model='all-MiniLM-L6-v2'):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.embedding_model = SentenceTransformer(embedding_model)
        self.index = None
        self.chunks_with_metadata = []

    def chunk_documents(self, documents):
        all_chunks = []
        for doc in documents:
            chunks = self.text_splitter.split_text(doc['text'])
            for chunk in chunks:
                all_chunks.append({'url': doc['url'], 'snippet': chunk})
        return all_chunks

    def create_index(self, documents, index_path="vector_index.faiss", metadata_path="chunks_metadata.json"):
        self.chunks_with_metadata = self.chunk_documents(documents)
        snippets = [item['snippet'] for item in self.chunks_with_metadata]
        
        print(f"Generating embeddings for {len(snippets)} chunks...")
        embeddings = self.embedding_model.encode(snippets, show_progress_bar=True)
        
        embedding_dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.index.add(np.array(embeddings, dtype=np.float32))
        
        print(f"Created index with {self.index.ntotal} vectors.")
        
        faiss.write_index(self.index, index_path)
        with open(metadata_path, 'w') as f:
            json.dump(self.chunks_with_metadata, f)
            
        return self.index.ntotal