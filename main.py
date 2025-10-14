# main.py

import argparse
import json
from crawler import Crawler
from indexer import Indexer
from qa_service import QAService

def run_crawl(args):
    crawler = Crawler(args.start_url, args.max_pages, args.crawl_delay_ms)
    pages = crawler.crawl()
    
    # Persist crawled data for the indexer
    with open("crawled_data.json", "w") as f:
        json.dump(pages, f)
        
    result = {"page_count": len(pages), "urls": [p['url'] for p in pages]}
    print(json.dumps(result, indent=2))

def run_index(args):
    with open("crawled_data.json", "r") as f:
        pages = json.load(f)
    
    indexer = Indexer(args.chunk_size, args.chunk_overlap)
    vector_count = indexer.create_index(pages)
    
    result = {"vector_count": vector_count, "errors": []}
    print(json.dumps(result, indent=2))

def run_ask(args):
    qa = QAService()
    response = qa.ask(args.question, args.top_k)
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple RAG service.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Crawl command [cite: 31]
    crawl_parser = subparsers.add_parser("crawl", help="Crawl a website.")
    crawl_parser.add_argument("start_url", type=str, help="The starting URL to crawl.")
    crawl_parser.add_argument("--max_pages", type=int, default=30, help="Maximum number of pages to crawl.")
    crawl_parser.add_argument("--crawl_delay_ms", type=int, default=500, help="Politeness delay in milliseconds.")
    crawl_parser.set_defaults(func=run_crawl)

    # Index command [cite: 32]
    index_parser = subparsers.add_parser("index", help="Index the crawled content.")
    index_parser.add_argument("--chunk_size", type=int, default=500, help="Size of text chunks.")
    index_parser.add_argument("--chunk_overlap", type=int, default=50, help="Overlap between chunks.")
    index_parser.set_defaults(func=run_index)

    # Ask command 
    ask_parser = subparsers.add_parser("ask", help="Ask a question based on the indexed content.")
    ask_parser.add_argument("question", type=str, help="The question to ask.")
    ask_parser.add_argument("--top_k", type=int, default=3, help="Number of chunks to retrieve for context.")
    ask_parser.set_defaults(func=run_ask)

    args = parser.parse_args()
    args.func(args)