import sys
from langchain_core.prompts import PromptTemplate
# from langchain.chains import RetrievalQA
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils.embeddings import initialize_embeddings_and_db
from langchain_community.chat_models import ChatLlamaCpp
# from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_chroma import Chroma
# from langchain_core.callbacks.base import BaseCallbackHandler


# class PrintRetrievalHandler(BaseCallbackHandler):
#     """
#     A callback handler for printing the status of context retrieval during a document search process. This handler updates the status container with the query, retrieved documents, and their metadata.

#     Attributes:
#         status: A status container object used for displaying retrieval status and document details.
#     """
#     def __init__(self, container):
#         self.status = container.status("**Context Retrieval**")

#     def on_retriever_start(self, serialized: dict, query: str, **kwargs):
#         self.status.write(f"**Question:** {query}")
#         self.status.update(label=f"**View Retrieved Sources:** {query}")

#     def on_retriever_end(self, documents, **kwargs):
#         for i, doc in enumerate(documents):
#             source = doc.metadata.get("source", "File directory not available.")
#             page_number = doc.metadata.get("page", "Page number not available.")
#             self.status.write(f"**Document {i+1}**")
#             self.status.markdown(f"**Source**: {source} **Page**: {page_number}")
#             self.status.markdown(doc.page_content)
#         self.status.update(state="complete")

class ChatPDFAssistant:
    """Handles PDF ingestion, query processing, and answering queries using a chat model."""

    def __init__(self, db="project_example", embeddings=None, llm=None):
        # Initialize embeddings and vector database
        _, self.client, self.vectordb, self.text_splitter, _ = initialize_embeddings_and_db(db)

        self.db = Chroma(client=self.client, collection_name="acunao-db",embedding_function=embeddings)

        # self.llm = ChatLlamaCpp(
        #     model_path = self.llm_model,
        #     n_gpu_layers = -1, 
        #     n_batch = 256,
        #     f16_kv = True,
        #     temperature = 0.0,
        #     n_ctx = 4500,
        #     streaming=True
        # )


        self.DEFAULT_SYSTEM_PROMPT = """
        You are a good, honest project assistant. 

        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you do not know the answer to a question, make it clear you do not know the answer instead of making up false information.
        """.strip()

        self.SYSTEM_PROMPT = "Use the following pieces of context to answer the question at the end. You must only answer within the provided context. If you do not know the answer, just say you don't know, don't try to make up an answer."

        self.template = self.generate_prompt(
            """
            {context}

            Question: {input}
            """,
            system_prompt=self.SYSTEM_PROMPT,
        )

        self.qa_prompt = PromptTemplate(template=self.template, input_variables=['context', 'input'])

        # Create QA Chain
        combine_docs_chain = create_stuff_documents_chain(llm, self.qa_prompt)
        self.chain = create_retrieval_chain(self.db.as_retriever(search_type="similarity", search_kwargs={"k": 3}), combine_docs_chain)

    def generate_prompt(self, prompt: str, system_prompt: str) -> str:
        return f"""
        <|system|>
        {system_prompt}<|end|>

        <|user|>
        {prompt}<|end|>
        """.strip()

    def chat(self, input_text):
        user_input = str(input_text)
        if user_input == 'exit':
            print('Exiting')
            sys.exit()
        if user_input == '':
            return None
        # result = self.chain.invoke({'input': user_input}, {"callbacks": st_cb})
        result = self.chain.invoke({"input":user_input})
        
        return result