# python-based-RAG-service
A small python based Retrieval‑Augmented Generation service 

This project is a small, command-line-based Retrieval-Augmented Generation (RAG) service. 
Given a starting URL, it can ingest website content, index it, and answer questions strictly based on the information it has collected, providing citations for its answers.

The primary focus of the project is on correctness, grounded responses, and clear engineering decisions.

# Architecture
The System is designed on three distinct stages
1. Ingestion: Crawling and fetching Web Content
2. Indexing: The ingested data is splitted into texts and then into chunks and a vector embedding is generated using 'sentence-transformers' and is stored in a 'FAISS' vector index for efficient similarity search.
3. Ask: The 'qa_service' module takes question from user and retrieves the most relevant chunks from the index which is then fed into LLM 'google/flan-t5-base' to generate an answer progided on the info  