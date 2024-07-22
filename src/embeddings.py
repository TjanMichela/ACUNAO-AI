import os
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.utils import embedding_functions
import shutil


def initialize_embeddings_and_db(folder_name):
    # Set the chunk size and overlap for text splitting
    chunk_size = 4500
    chunk_overlap = 1000

    # Specify the desktop path and folder name for vector database storage
    desktop_path = os.path.join(os.path.expanduser("~"), "Documents", "ACUNAO-Data")
    vdb_name = "vectordb"
    folder_path = os.path.join(desktop_path, folder_name, vdb_name)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if folder_name == "project_example":
        src_folder_path = "./data/2_test_data"
        dest_folder_path = os.path.join(desktop_path, folder_name)
        for item in os.listdir(src_folder_path):
            s = os.path.join(src_folder_path, item)
            d = os.path.join(dest_folder_path, item)

            # Skip .md files
            if os.path.isfile(s) and s.endswith('.md'):
                continue
            
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
    
    # Initialize embeddings
    embeddings = embedding_functions.SentenceTransformerEmbeddingFunction("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)

    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # Initialize Chroma vector store or load existing if available
    client = chromadb.PersistentClient(folder_path)
    collection = client.get_or_create_collection(name="acunao-db", embedding_function=embeddings)

    return embeddings, client, collection, text_splitter