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
        self.process_start = False
        self.process_end = False

    def on_any_event(self, event):
        normalized_path = os.path.normpath(event.src_path)
        path_parts = normalized_path.split(os.sep)
        
        if event.is_directory or not event.src_path.endswith(tuple(self.processor.supported_extensions)):
            return None

        database_index = path_parts.index("ACUNAO-Data")
        subpath_parts = path_parts[database_index + 1:]
        if subpath_parts and os.path.splitext(subpath_parts[-1])[1]:
            subpath_parts = subpath_parts[:-1]
        self.processor.folder_name = os.sep.join(subpath_parts)

        if len(self.processor.folder_name) != 0: 
            if event.event_type in ['created', 'modified']:
                if not self.process_start:  # Only process if not already processing
                    self.process_start = True
                    self.processor.embeddings, self.processor.client, self.processor.vectordb, self.processor.text_splitter = initialize_embeddings_and_db(self.processor.folder_name)
                    self.processor.update_vector_db(event.src_path)
                    self.process_end = True

            elif event.event_type == 'deleted':
                self.processor.embeddings, self.processor.client, self.processor.vectordb, self.processor.text_splitter = initialize_embeddings_and_db(self.processor.folder_name)
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
        self.desktop_path = os.path.join(os.path.expanduser("~"), "Documents", "ACUNAO-Data")
        self.folder_name = "project_example" 
        self.folder_path = os.path.join(self.desktop_path, self.folder_name)
        self.vectordb = None
        self.embeddings = None
        self.text_splitter = None
        self.files = []
        self.observer = None
        self.event_handler = None
        self.observer_initialized = False
        self.observer_thread = None
        self.supported_extensions = [".pdf"]
        self.loaded_files_path = os.path.join(self.folder_path, "processed_files.txt")
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
            self.observer.schedule(self.event_handler, self.desktop_path, recursive=True)
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
        self.embeddings, self.client, self.vectordb, self.text_splitter = initialize_embeddings_and_db(self.folder_name)
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