# Obsidian RAG Prototype

This repository contains a prototype for a Retrieval-Augmented Generation (RAG) system using Obsidian markdown files. The system uses FAISS for efficient similarity search and OpenAI's GPT models for generating responses.

## Setup

### Prerequisites

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
- [Python 3.10](https://www.python.org/downloads/)
- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/obsidian-RAG.git
cd obsidian-RAG
```

2. Create and activate a new conda environment:
```bash
conda env create -f environment.yaml
conda activate rag-env
```

3. Install the required Python packages:
```bash
poetry init
poetry install
```

4. Create a .env file in the root directory and add your enviornment variables
# .env
OPENAI_API_KEY='your-openai-api-key'
MARKDOWN_DIR='your-vault-directory'
OUTPUT_FILE_PATH='location-to-save-all-vault-as-doc'
FAISS_INDEX_PATH='location-to-save-FAISS-index'

### Usage
##### Loading Markdown Files
Run the markdown.py script to load markdown files from the specified directory and save them to a pickle file:

##### Creating FAISS Index
Run the faiss_index.py script to create a FAISS index from the loaded markdown files:

#### Querying the System
Run the query.py script to query the system and get responses from the OpenAI model:

#### Running the NiceGUI App
Run the app.py script to start the NiceGUI application:

#### Contributing
Contributions are welcome! Please open an issue or submit a pull request.

#### License
This project is licensed under the MIT License.



