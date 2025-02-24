from openai import OpenAI


import os
import faiss    
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
from dotenv import load_dotenv

load_dotenv()

# Get the directory paths from environment variables
markdown_dir = os.getenv('MARKDOWN_DIR')
output_file_path = os.getenv('OUTPUT_FILE_PATH')
faiss_index_path = os.getenv('FAISS_INDEX_PATH')
client = OpenAI(
  api_key=os.getenv('OPENAI_API_KEY')
)

docs = pickle.load(open(output_file_path, 'rb'))

# Function to load the FAISS index
def load_faiss_index(index_path):
    return faiss.read_index(index_path)

# Load the FAISS index
index = load_faiss_index(faiss_index_path)
model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_relevant_docs(query, k=15):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)
    # Filter out invalid indices
    valid_results = []
    for i in indices[0]:
        if 0 <= i < len(docs):
            valid_results.append(docs[i])
        else:
            # Optionally, log or handle the invalid index
            print(f"Invalid index encountered: {i}")
    return valid_results


def generate_response(query):
    # Retrieve relevant documents
    relevant_docs = retrieve_relevant_docs(query)
    context = "\n\n".join([f"File: {doc}" for doc in relevant_docs])

    # Construct the prompt
    prompt = f"Answer the following question based on the context:\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"

    messages=[
        {"role": "assistant", 
        "content": "you are an personal assistant to help me retrieve relevant information from my personal obsidian vault"},
        {
            "role": "user",
            "content": f"{prompt}"
        }
    ]
    # Generate response
    response = client.chat.completions.create(model="gpt-4o",  # Or gpt-4 if available
    messages=messages,
    max_tokens=500)
    return context, response.choices[0].message.content

if __name__ == "__main__":
    query = "What are my 2025 resolutions?"
    response = generate_response(query)
    # print(f"here is the context: {response[0]}")
    print(f"Question: {query}\nAnswer: {response[1]}")

    # result = retrieve_relevant_docs(query)
    # print(result)