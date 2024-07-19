import os
from embeddings import initialize_embeddings_and_db
from pdfparser import PDFLoader
from langchain_community.vectorstores.utils import filter_complex_metadata
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import uuid
import hashlib
import logging
import time


desktop_path = os.path.join(os.path.expanduser("~"), "Documents")
folder_name = "ACUNAO-Data"
folder_path = os.path.join(desktop_path, folder_name)
vdb_path = os.path.join(folder_path, "vectordb")
PROCESSED_FILES_HASH = os.path.join(folder_path, "processed_files.txt") 

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

class DocumentEventHandler(FileSystemEventHandler):
    """
    A custom event handler for monitoring and processing document-related events in a file system. This handler processes files with specific extensions and triggers actions on create, modify, and delete events.
    
    Attributes:
        processor: An instance responsible for processing and updating the vector database.
        supported_extensions: A set of file extensions that the handler will process.
        process_start: A flag indicating the processing state.
    """
    def __init__(self, processor):
        self.processor = processor
        # self.supported_extensions = {".pdf", ".docx", ".pptx", ".xlsx", ".md", ".txt"}
        self.supported_extensions = {".pdf"}
        self.process_start = 0

    def on_any_event(self, event):
        if event.is_directory or not event.src_path.endswith(tuple(self.supported_extensions)):
            return None
        if event.event_type in ['created', "modified"]:
            self.process_start = 1
            self.processor.update_vector_db(event.src_path)
            self.process_start = 2
        elif event.event_type == "deleted":
            self.processor.delete_from_vector_db(event.src_path)

class DocumentProcessor:
    """
    A class responsible for processing documents, managing embeddings, and interfacing with a vector database. This class initializes necessary components and sets up a file system observer for monitoring changes in the specified folder path.

    Attributes:
        embeddings: Placeholder for document embeddings.
        vectordb: Path to the vector database.
        text_splitter: Placeholder for a text splitting utility.
        folder_path: Path to the folder containing documents to be processed.
        files: List to hold the names of the files to be processed.
        observer: Observer for monitoring file system changes.
        event_handler: Event handler for processing document-related events.
        observer_initialized: Flag indicating whether the observer has been initialized.
        observer_thread: Thread for running the observer.
        supported_extensions: List of file extensions that the processor will handle.
        loaded_files_path: Path to the file containing hashes of already processed files.
        loaded_files: Set of hashes of already processed files, loaded from the specified path.
    """
    def __init__(self):
        self.embeddings = None
        self.vectordb = vdb_path
        self.text_splitter = None
        self.folder_path = folder_path
        self.files = []
        self.observer = None
        self.event_handler = None
        self.observer_initialized = False
        self.observer_thread = None
        # self.supported_extensions = [".pdf", ".docx", ".pptx", ".xlsx", ".md", ".txt"]
        self.supported_extensions = [".pdf"]
        self.loaded_files_path = PROCESSED_FILES_HASH
        self.loaded_files = self.load_loaded_files()

    def load_loaded_files(self):
        if os.path.exists(self.loaded_files_path):
            with open(self.loaded_files_path, 'r') as f:
                return set(f.read().splitlines())
        else:
            return set()

    def save_loaded_files(self):
        with open(self.loaded_files_path, 'w') as f:
            f.write('\n'.join(self.loaded_files))

    def initialize_observer(self):
        if not self.observer_initialized:
            self.observer = Observer()
            self.event_handler = DocumentEventHandler(self)
            self.observer.schedule(self.event_handler, self.folder_path, recursive=True)
            self.observer.start()
            self.observer_initialized = True

    def file_hash(self, file_path):
        """
        Generate a hash for a file.
        """
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def update_vector_db(self, file_path):
        file_extension = os.path.splitext(file_path)[1]
        doc_hash = self.file_hash(file_path)

        # Skip files that have already been processed
        if doc_hash in self.loaded_files:
            logging.info("Skipping already processed file: %s", file_path)
            return

        elif file_extension in self.supported_extensions and file_path not in self.loaded_files:
            print("Changes detected in folder. Updating vector database...")

            logging.info("Processing file: %s", file_path)

            loader = PDFLoader(file_path)

            documents = loader.load()
            text_chunks = filter_complex_metadata(self.text_splitter.split_documents(documents))

            self.vectordb.add(
                documents=[doc.page_content for doc in text_chunks],
                metadatas=[doc.metadata for doc in text_chunks],
                ids=[str(uuid.uuid4()) for _ in range(len(text_chunks))]
            )

            logging.info("File processed: %s", file_path)
            self.loaded_files.add(doc_hash)
            self.save_loaded_files()

        else:
            logging.warning("Unsupported file type or already loaded: %s", file_path)

    def delete_from_vector_db(self, file_path):
        file_extension = os.path.splitext(file_path)[1]
        doc_hash = self.file_hash(file_path)
        if file_extension in self.supported_extensions:
            file_id = os.path.basename(file_path)
            print(f"File deleted: {file_path}. Removing from vector database...")
            self.vectordb.delete(ids=[file_id])
            self.loaded_files.discard(doc_hash)
            self.save_loaded_files()
        else:
            print(f"File deleted: {file_path}. Extension not supported, skipping deletion from vector database.")

    def run(self):
        self.embeddings, self.client, self.vectordb, self.text_splitter = initialize_embeddings_and_db()
        if not self.observer_initialized:
            self.initialize_observer()

        try:
            print("Running document processor. Press Ctrl+C to stop.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted by user. Stopping...")
        except Exception as error:
            print("Error processing documents: " + str(error))
        finally:
            self.stop_observer()

    def stop_observer(self):
        if self.observer_initialized:
            self.observer.stop()
            self.observer.join()
            print("Stopped the observer and saved state.")
            self.observer_initialized = False