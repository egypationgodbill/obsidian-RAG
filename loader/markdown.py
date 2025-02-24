import os
import pickle
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

markdown_dir = os.getenv('MARKDOWN_DIR')
output_file_path = os.getenv('OUTPUT_FILE_PATH')
metadata_file = os.getenv("PROCESS_FILE_PATH")  # Stores processed file timestamps


def load_existing_metadata(metadata_path):
    """Load previously processed file metadata (timestamps)."""
    if os.path.exists(metadata_path):
        with open(metadata_path, "rb") as f:
            return pickle.load(f)
    return {}


def save_metadata(metadata, metadata_path):
    """Save processed file metadata."""
    with open(metadata_path, "wb") as f:
        pickle.dump(metadata, f)


def load_markdown_files(directory, existing_metadata):
    """Load only new or updated markdown files."""
    docs = []
    filenames = []
    new_metadata = {}

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".md"):
                file_path = os.path.join(root, filename)
                file_mtime = os.path.getmtime(file_path)  # Get file modification time
                
                # Check if the file is new or modified
                if file_path not in existing_metadata or existing_metadata[file_path] < file_mtime:
                    with open(file_path, "r", encoding="utf-8") as f:
                        docs.append(f.read())
                        filenames.append(file_path)

                # Update metadata
                new_metadata[file_path] = file_mtime

    return docs, filenames, new_metadata


# Load existing metadata
existing_metadata = load_existing_metadata(metadata_file)

# Load new/updated markdown files
docs, filenames, new_metadata = load_markdown_files(markdown_dir, existing_metadata)

if docs:
    # Save updated documents
    with open(output_file_path, "wb") as f:
        pickle.dump(docs, f)

    # Save updated metadata
    save_metadata(new_metadata, metadata_file)

    print(f"Processed {len(docs)} updated/new markdown files and saved to {output_file_path}.")
else:
    print("No new or updated markdown files detected.")