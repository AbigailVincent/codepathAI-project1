import chromadb
from sentence_transformers import SentenceTransformer
 
CHROMA_DIR      = "./vectorstore"
COLLECTION_NAME = "unofficial_guide"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 4   # matches your planning.md value
 
# Distance score guide (cosine, lower = more similar):
#   < 0.30  → strong match
#   0.30–0.50 → decent match
#   0.50–0.70 → weak — read the chunk and judge manually
#   > 0.70  → likely a miss
WARN  = 0.50
FAIL  = 0.70
 
# ── Load model and collection once at startup ─────────────────────────────────
print("Loading model and vector store...")
_model      = SentenceTransformer(EMBEDDING_MODEL)
_client     = chromadb.PersistentClient(path=CHROMA_DIR)
_collection = _client.get_collection(COLLECTION_NAME)
print(f"  {_collection.count()} chunks loaded\n")
 
 
def retrieve(query: str, k: int = TOP_K) -> list:
    """
    Find the top-k chunks most semantically similar to the query.
 
    How it works:
      1. Embed the query with the same model used at index time.
         Both the query and chunks live in the same 384-dim vector space.
      2. ChromaDB computes cosine distance to every stored chunk.
      3. Return the k nearest — lower distance means more similar meaning.
 
    This is why a query like "difficult exams" can match a chunk saying
    "exams are reviewed to be difficult" even with no shared words.
 
    Returns list of dicts: text, source, chunk_number, distance
    """
    query_vector = _model.encode(query).tolist()
 
    # [0] unpacks results for our single query (ChromaDB supports batching)
    results = _collection.query(
        query_embeddings=[query_vector],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
 
    return [
        {
            "text":         text,
            "source":       meta.get("source", "unknown"),
            "chunk_number": meta.get("chunk_number", -1),
            "distance":     round(dist, 4),
        }
        for text, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]
 
 
def print_results(query: str, results: list) -> None:
    print(f"\n{'=' * 62}")
    print(f"QUERY: {query}")
    print(f"{'=' * 62}")
 
    for rank, chunk in enumerate(results, start=1):
        d    = chunk["distance"]
        flag = "✓ good" if d < WARN else ("~ ok" if d < FAIL else "⚠ weak")
        print(f"\n  Rank {rank}  |  distance: {d}  |  {flag}")
        print(f"  Source: {chunk['source']}  (chunk #{chunk['chunk_number']})")
        print(f"  {'-' * 56}")
        print(f"  {chunk['text']}")
 
    top = results[0]["distance"] if results else 99
    if top > FAIL:
        print(f"\n  ⚠  Best distance is {top} — retrieval is struggling.")
        print(  "     With short single-sentence chunks this is expected for")
        print(  "     queries that use different words than your documents.")
        print(  "     Document this in your evaluation report as a failure case.")
 
 
# ── Your 5 evaluation plan queries from planning.md ──────────────────────────
# These match your planning.md exactly. Run all 5 here — the milestone only
# requires 3 but running all 5 now saves time in Milestone 6.
 
EVAL_QUERIES = [
    "Which professors have difficult exams?",
    "Which professors are helpful or easy to contact during office hours?",
    "Which professors are considered fair graders?",
    "Which courses have difficult homework?",
    "Which professor has light or fun or easy or summarized lectures?",
]
 
 
if __name__ == "__main__":
    print(f"=== Milestone 4: Retrieval test  (k={TOP_K}) ===\n")
 
    for query in EVAL_QUERIES:
        results = retrieve(query)
        print_results(query, results)
 
    # ── Checkpoint summary ────────────────────────────────────────────────────
    print(f"\n\n{'=' * 62}")
    print("MILESTONE 4 CHECKPOINT")
    print(f"{'=' * 62}")
    print("For each query above, verify:")
    print("  [ ] Returned chunks mention the right professor(s)")
    print("  [ ] Source filename on every result matches the professor")
    print("  [ ] Top result distance is below 0.50 on most queries")
    print("")
    print("Known hard query for your corpus:")
    print("  Q2 (office hours) — 5 professors described with different words:")
    print("  'useful', 'helped them', 'easy to contact', 'determination',")
    print("  'helpful office hours'. Short chunks may miss some of these.")
    print("  If it only retrieves 2-3 of the 5, document it as a partial")
    print("  failure in your evaluation report — that's honest and expected.")
