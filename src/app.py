import os
import streamlit as st
from loader import DocumentProcessor
from llm import ChatPDFAssistant, PrintRetrievalHandler
import subprocess
import platform
import threading
import time
from langchain.callbacks.streamlit import StreamlitCallbackHandler

def setup_streamlit_page():
    """
    Configures the default settings of the page.
    """
    st.set_page_config(page_title="💬 ACUNAO Chatbot", layout="wide")

def setup_chat_page(assistant):
    """
    Configures the settings of the chat section of the page. It contains the title, instructions to start using the chatbot, and interactions between the AI assistant and the user. Queries and responses happen in this function.
    """

    st.title("💬 ACUNAO Chatbot")

    st.info(
        """
        **Welcome! How may I assist you today?**  
        Start by adding supported documents into the ACUNAO-Data folder in your computer's Documents folder or click the `Open Folder` button in the sidebar. ACUNAO currently supports PDF documents:  

        1. Open your computer's Documents folder.  
        2. Create a new folder with your project name to create a new project  
        3. Add documents into the folder and your AI assistant is ready to answer your questions!   

        **Pro tip:** Organize your project by creating separate folders for different topics inside your project to create separate databases!""")

    if "messages" not in st.session_state.keys():
        # Set the initial AI message
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    for message in st.session_state.messages:
        # Display queries and responses
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            retrieval_handler = PrintRetrievalHandler(st.container()) # Callback for retriever
            st_cb = StreamlitCallbackHandler(
                            st.container(),
                            collapse_completed_thoughts=True,
                            expand_new_thoughts=True,
                            ) # Callback for RAG chain
            response = assistant.chat(prompt, st_cb=[st_cb, retrieval_handler])
            st.markdown(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)

def open_folder(path):
    """
    Opens the folder that houses the database and documents used in the RAG system.
    """
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", path])
    else:  # Linux
        subprocess.Popen(["xdg-open", path])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

def setup_sidebar():
    """
    Configures the settings of the sidebar. It contains basic information about the AI assistant, lists the supported documents users added into the ACUNAO-Data folder, and button to clear chat history.
    """
    st.sidebar.title("💬 ACUNAO Chatbot")
    st.sidebar.subheader("Chat with your documents")
    st.sidebar.markdown(
        """An AI assistant programmed to answer questions and provide information based on the documents you provide. It will only answer within the context you provide and should not deviate from the documents provided. If the AI assistant's answer is not based on the context, please let our lab know."""
        )

    # Specify the desktop path and folder name for files storage
    desktop_path = os.path.join(os.path.expanduser("~"), "Documents")
    folder_name = "ACUNAO-Data"
    folder_path = os.path.join(desktop_path, folder_name)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Define supported file extensions
    # supported_extensions = {".pdf", ".docx", ".pptx", ".xlsx", ".md", ".txt"}
    supported_extensions = {".pdf"}

    # List files with supported extensions in the folder
    files = [file for file in os.listdir(folder_path) if not file.startswith('.') and os.path.splitext(file)[1] in supported_extensions]
    
    # Display files in sidebar with options to delete
    st.sidebar.subheader("Available Documents")
    st.sidebar.success("Connected to ACUNAO-Data folder", icon="✅")

    for file in files:
        col1, col2 = st.sidebar.columns([4, 1])
        col1.write(file)

    if st.sidebar.button("Open Folder"):
        open_folder(folder_path)

    st.sidebar.divider()

    st.sidebar.subheader("Manage Chat History")
    st.sidebar.warning("Warning: your chat history will be cleared from memory!", icon="⚠️")
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history, type="secondary")
    
    return None

@st.cache_resource
def init_assistant():
    assistant = ChatPDFAssistant()
    return assistant

@st.cache_resource
def init_processor():
    processor = DocumentProcessor()
    return processor

def main():
    setup_streamlit_page()
    setup_sidebar()

    assistant = init_assistant()
    processor = init_processor()

    processor_thread = threading.Thread(target=processor.run, daemon=True)
    processor_thread.start()

    setup_chat_page(assistant)

    while processor_thread.is_alive():
        # Display status of document processing 
        time.sleep(2)
        if processor.event_handler is not None:
            try:
                placeholder = st.empty()
                if processor.event_handler.process_start == 1:
                    placeholder.warning("New document detected!")
                    time.sleep(5)
                    placeholder.warning("Processing document...")
                    processor.event_handler.process_start = 0
                elif processor.event_handler.process_start == 2:
                    st.success("Done! Finished processing document.", icon="✅")
                    processor.event_handler.process_start = 0
                else:
                    continue
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    main()
