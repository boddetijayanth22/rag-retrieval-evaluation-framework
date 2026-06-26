"""
Configuration File:
Change only these values when running experiments.
"""

# PDF Configuration
PDF_PATH = "sample.pdf"

# ChromaDB Configuration
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "rag_collection"

# Chunking Configuration
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# Retrieval Configuration
TOP_K = 3

# Embedding Model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"