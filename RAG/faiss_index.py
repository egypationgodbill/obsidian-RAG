from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle
import time
import os
from dotenv import load_dotenv
# Load documents from pickle file
# Load environment variables from .env file
load_dotenv()

# Get the directory paths from environment variables
output_file_path = os.getenv('OUTPUT_FILE_PATH')
faiss_index_path = os.getenv('FAISS_INDEX_PATH')
docs = pickle.load(open(output_file_path, 'rb'))

t0 = time.time()
# Load pre-trained embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # A lightweight, efficient model

# Embed the documents
doc_embeddings = model.encode(docs)
print(f"Embedded {len(docs)} documents in {time.time() - t0:.2f} seconds.")

# Create a FAISS index
t0 = time.time()
index = faiss.IndexFlatL2(doc_embeddings.shape[1])  # L2 distance
index.add(np.array(doc_embeddings))
print(f"Created FAISS index in {time.time() - t0:.2f} seconds.")

# Save the FAISS index to a file
faiss.write_index(index, faiss_index_path)  # Replace with your desired output file path

