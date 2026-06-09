import chromadb
from sentence_transformers import SentenceTransformer
from collections import Counter
 
# Import your existing ingestion pipeline
from ingestion import load_documents, create_chunks
 
DOCUMENTS_FOLDER = "documents"
CHROMA_DIR       = "./vectorstore"
COLLECTION_NAME  = "unofficial_guide"
EMBEDDING_MODEL  = "all-MiniLM-L6-v2"
 
 
def build_vector_store(chunks: list) -> chromadb.Collection:
    """
    Embed every chunk and store it in ChromaDB with source metadata.
 
    ChromaDB stores three things per chunk:
      - embedding vector  → used at query time to find similar chunks
      - document text     → returned with results so you can read the chunk
      - metadata          → source filename + chunk_number for attribution
 
    The embedding model maps text to a 384-dimensional vector.
    Two chunks that mean similar things land near each other in that space
    even if they share no exact words — that's why "difficult exams" matches
    "exams are reviewed to be difficult" (Professor Amanda).
    """
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
 
    print(f"Connecting to ChromaDB at: {CHROMA_DIR}")
    client = chromadb.PersistentClient(path=CHROMA_DIR)
 
    # get_or_create_collection is safe to re-run — won't duplicate data.
    # cosine distance is standard for sentence embeddings: it measures
    # the angle between two vectors, not their magnitude, which works well
    # when chunks vary in length (yours do — 1 sentence vs 3 sentences).
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
 
    print(f"\nEmbedding {len(chunks)} chunks...")
    texts = [chunk["text"] for chunk in chunks]
 
    # Encode all chunks in one batch — much faster than one at a time
    embeddings = model.encode(texts, show_progress_bar=True)
 
    # Each ID must be unique across the whole collection.
    # chunk_number alone isn't unique because it resets to 0 per document.
    # Combining source + chunk_number gives e.g. "professor1.txt_chunk_0"
    ids = [f"{chunk['source']}_chunk_{chunk['chunk_number']}" for chunk in chunks]
 
    collection.add(
        ids        = ids,
        embeddings = embeddings.tolist(),   # ChromaDB needs plain Python lists
        documents  = texts,
        metadatas  = [
            {
                "source":       chunk["source"],
                "chunk_number": chunk["chunk_number"],
            }
            for chunk in chunks
        ],
    )
 
    print(f"\n✓ Stored {collection.count()} chunks in '{COLLECTION_NAME}'")
    return collection
 
 
def verify_load(collection: chromadb.Collection, chunks: list) -> None:
    """Print a summary so you can catch load problems before querying."""
    stored   = collection.count()
    expected = len(chunks)
 
    print(f"\n=== Load verification ===")
    print(f"  Expected: {expected}  |  Stored: {stored}", end="  ")
    print("✓" if stored == expected else "⚠ MISMATCH — check for duplicate IDs")
 
    # Show chunk counts per source — confirms all 10 files loaded
    all_meta = collection.get(include=["metadatas"])["metadatas"]
    counts   = Counter(m["source"] for m in all_meta)
    print(f"\n  Chunks per source file:")
    for source, count in sorted(counts.items()):
        print(f"    {source}: {count} chunks")
 
    # Confirm source metadata is present (needed for attribution in Milestone 5)
    sample = collection.peek(limit=1)
    if sample["metadatas"] and "source" in sample["metadatas"][0]:
        print(f"\n  ✓ Source metadata present on chunks")
    else:
        print(f"\n  ⚠ WARNING: 'source' key missing — fix before Milestone 5")
 
 
if __name__ == "__main__":
    print("=== Building vector store ===\n")
    documents = load_documents(DOCUMENTS_FOLDER)
    chunks    = create_chunks(documents)
 
    if not chunks:
        print("ERROR: No chunks found. Is the documents/ folder populated?")
        raise SystemExit(1)
 
    collection = build_vector_store(chunks)
    verify_load(collection, chunks)
    print("\n✓ Done. Run retrieve.py to test your queries.")
