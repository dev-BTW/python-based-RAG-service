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

# Requirements and setup
1. Python 3.11 or above
2.  The following libraries
    * requests
    * beautifulsoup4
    * trafilatura
    * langchain
    * sentence-transformers
    * numpy
    * faiss-cpu
    * transformers
    * torch
    * accelerate

# Steps
1. Clone the repo and create a virtual env
    ```python -m venv mvenv```

2. Install dependencies
    ```pip install -r requirements.txt```

3. python main.py crawl website --max_pages no. of pages
   ```python main.py crawl http://books.toscrape.com --max_pages 50```
   Note:- Only use http protocol

4. ```python main.py index```

5. python main.py ask "question"
   ```python main.py ask "Which books are in the 'Mystery' category?"```


# Trade-offs 
### Chose simplicity over robustness of data
* In memory vector store:- Increased searching speed at the cost of scalability
* Open source:- Gained total control at the cost of performance and 
* No data cleaning:- Less computation and load on the system, ignoring the quality of data affecting the final output

# Limitations
* Limited scalability 
* Necessary to index the data every time
* CLI-based, which is not suitable for regular users
* Can only process static data
