import json
import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


class RAGManager:
    def __init__(self):
        # Using a stable Google Generative AI embedding model
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="text-embedding-004", google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )

    def ingest_cv(self, pdf_path: str):
        """Processes the CV PDF file and adds it to the vector store."""
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        chunks = self.text_splitter.split_documents(docs)

        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        else:
            self.vector_store.add_documents(chunks)

        return len(chunks)

    def ingest_qa(self, qa_path: str):
        """Processes the Q&A knowledge base (JSON) and adds it to the vector store."""
        if not os.path.exists(qa_path):
            return 0

        with open(qa_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Convert Q&A into formatted documents
        qa_docs = []
        for item in data:
            content = f"Question: {item['question']}\nAnswer: {item['answer']}"
            qa_docs.append(content)

        chunks = self.text_splitter.create_documents(qa_docs)

        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        else:
            self.vector_store.add_documents(chunks)

        return len(chunks)

    def get_retriever(self):
        """Returns a retriever object from the initialized vector store."""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Please ingest data first.")
        return self.vector_store.as_retriever(search_kwargs={"k": 5})

    def save_local(self, folder_path: str):
        """Saves the vector store locally."""
        if self.vector_store:
            self.vector_store.save_local(folder_path)

    def load_local(self, folder_path: str):
        """Loads a vector store from a local folder."""
        self.vector_store = FAISS.load_local(
            folder_path, self.embeddings, allow_dangerous_deserialization=True
        )
