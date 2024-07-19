import os
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.utils import embedding_functions

# Set the chunk size and overlap for text splitting
chunk_size = 4500
chunk_overlap = 1000

def initialize_embeddings_and_db():
    # Initialize embeddings
    embeddings = embedding_functions.SentenceTransformerEmbeddingFunction("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)

    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # Specify the desktop path and folder name for vector database storage
    desktop_path = os.path.join(os.path.expanduser("~"), "Documents", "Kunye-Data")
    folder_name = "vectordb"
    folder_path = os.path.join(desktop_path, folder_name)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Initialize Chroma vector store or load existing if available
    client = chromadb.PersistentClient(folder_path)
    collection = client.get_or_create_collection(name="kunye-db", embedding_function=embeddings)

    return embeddings, client, collection, text_splitter