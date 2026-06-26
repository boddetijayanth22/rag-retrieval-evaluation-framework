import chromadb

from config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

from pdf_loader import load_pdf
from chunker import create_chunks

def build_index():
    """
    Builds a ChromaDB vector index from the PDF.
    """

    print("=" * 100)
    print("BUILDING VECTOR INDEX")
    print("=" * 100)

    # Load PDF

    print("\nLoading PDF...")

    text = load_pdf()

    print(" PDF Loaded")

    # Create Chunks

    print("\n Creating Chunks...")

    chunks = create_chunks(text)

    print(f" Total Chunks : {len(chunks)}")

    # Create Chroma Client

    client = chromadb.PersistentClient(
        path=CHROMA_DB_PATH
    )

    # Remove Existing Collection
    try:
        client.delete_collection(COLLECTION_NAME)
        print("\n Old Collection Deleted")
    except:
        print("\n No Existing Collection Found")

    # Create Collection

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={
            "hnsw:space": "cosine"
        }
    )

    print(" New Collection Created")

    # Prepare IDs

    ids = []

    for i in range(len(chunks)):
        ids.append(f"chunk_{i}")

    # Prepare Metadata

    metadatas = []

    for i in range(len(chunks)):

        metadatas.append(
            {
                "chunk_id": i,
                "source": "sample.pdf",
                "chunk_size": CHUNK_SIZE,
                "overlap": CHUNK_OVERLAP,
            }
        )

    # Store Documents

    print("\n Generating Embeddings & Storing...")

    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas,
    )

    print(" Index Built Successfully")

    # Summary

    print("\n" + "=" * 100)

    print("INDEX SUMMARY")

    print("=" * 100)

    print(f"Collection Name : {COLLECTION_NAME}")
    print(f"Stored Chunks   : {collection.count()}")
    print(f"Chunk Size      : {CHUNK_SIZE}")
    print(f"Overlap         : {CHUNK_OVERLAP}")

    print("=" * 100)

    return collection

if __name__ == "__main__":
    build_index()