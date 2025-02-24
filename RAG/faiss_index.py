from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle
import time
import os
import hashlib
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the directory paths from environment variables
output_file_path = os.getenv('OUTPUT_FILE_PATH')
faiss_index_path = os.getenv('FAISS_INDEX_PATH')
metadata_path = os.getenv('METADATA_PATH', 'index_metadata.json')

# Load all documents from pickle file
docs = pickle.load(open(output_file_path, 'rb'))

def compute_doc_hash(doc: str) -> str:
    """Compute an MD5 hash for a given document string."""
    return hashlib.md5(doc.encode('utf-8')).hexdigest()

def load_metadata(meta_path: str) -> dict:
    try:
        with open(meta_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(meta: dict, meta_path: str):
    with open(meta_path, 'w') as f:
        json.dump(meta, f)

# Load existing metadata (document hashes) if available
metadata = load_metadata(metadata_path)

# Identify new documents
new_docs = []
for doc in docs:
    doc_hash = compute_doc_hash(doc)
    if doc_hash not in metadata:
        new_docs.append(doc)
        # Mark document as indexed
        metadata[doc_hash] = True

# Load pre-trained embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # A lightweight, efficient model

# Check if an existing FAISS index exists; if not, create one from scratch
if os.path.exists(faiss_index_path):
    index = faiss.read_index(faiss_index_path)
    print("Loaded existing FAISS index.")
else:
    # Compute embeddings for all docs if no index exists
    t0 = time.time()
    doc_embeddings = model.encode(docs)
    print(f"Embedded {len(docs)} documents in {time.time() - t0:.2f} seconds.")
    index = faiss.IndexFlatL2(doc_embeddings.shape[1])  # L2 distance
    index.add(np.array(doc_embeddings))
    print("Created FAISS index from scratch.")

# If any new documents were found, compute embeddings for them and add them to the index
if new_docs:
    t0 = time.time()
    new_embeddings = model.encode(new_docs)
    index.add(np.array(new_embeddings))
    print(f"Embedded {len(new_docs)} new documents in {time.time() - t0:.2f} seconds and updated the index.")
    # Save the updated metadata and index
    save_metadata(metadata, metadata_path)
    faiss.write_index(index, faiss_index_path)
else:
    print("No new documents found; index is up-to-date.")

print(f"FAISS index now contains {index.ntotal} documents.")