

import os
import pickle
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Get the directory paths from environment variables
markdown_dir = os.getenv('MARKDOWN_DIR')
output_file_path = os.getenv('OUTPUT_FILE_PATH')
def load_markdown_files(directory):
    docs = []
    filenames = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".md"):
                with open(os.path.join(root, filename), "r", encoding="utf-8") as f:
                    docs.append(f.read())
                    filenames.append(os.path.join(root, filename))
    return docs, filenames

# markdown_dir = "path/to/obsidian_notes"  # Replace with your Obsidian notes directory
def save_docs_to_file(docs, output_file):
    with open(output_file, "wb") as f:
        pickle.dump(docs, f)

docs, filenames = load_markdown_files(markdown_dir)
save_docs_to_file(docs, output_file_path)

print(f"Loaded {len(docs)} markdown files and saved them to {output_file_path}.")