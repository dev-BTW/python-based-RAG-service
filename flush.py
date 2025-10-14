import os

def flush_generated_files():
    """
    Deletes the auto-generated files from the RAG pipeline.

    This script safely removes the data files created during the crawl
    and index stages, allowing for a clean start.
    """
    files_to_delete = [
        "crawled_data.json",
        "vector_index.faiss",
        "chunks_metadata.json"
    ]

    print("--- Starting Cleanup ---")
    
    for filename in files_to_delete:
        try:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"🗑️  Deleted: {filename}")
            else:
                print(f"⚪  Not found (already clean): {filename}")
        except OSError as e:
            print(f"❌ Error deleting {filename}: {e}")

    print("--- Cleanup Complete ---")

if __name__ == "__main__":
    flush_generated_files()
