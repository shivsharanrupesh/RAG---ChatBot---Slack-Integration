"""
PDF Ingestion Script for RAG IT Support Chatbot

- Loads all PDFs in the data directory.
- Splits into chunks.
- Embeds text using Cohere embeddings.
- Stores vectors in ChromaDB, with optional persistent storage.

Run: python app/ingest.py
"""

import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import CohereEmbeddings

DATA_DIR = "data"

def get_cohere_api_key():
    """
    Get the Cohere API key from the environment.
    Raises:
        EnvironmentError: if the key is not set.
    Returns:
        str: The Cohere API key.
    """
    key = os.environ.get("COHERE_API_KEY")
    if not key:
        raise EnvironmentError("COHERE_API_KEY environment variable is not set!")
    return key

def get_vectordb(embeddings):
    """
    Returns a Chroma vector store instance.
    Uses persistent directory if CHROMA_DB_DIR is set and exists.
    Otherwise, uses in-memory store.
    """
    chroma_db_dir = os.getenv("CHROMA_DB_DIR")
    if chroma_db_dir and os.path.isdir(chroma_db_dir):
        vectordb = Chroma(persist_directory=chroma_db_dir, embedding_function=embeddings)
    else:
        vectordb = Chroma(embedding_function=embeddings)
    return vectordb

def ingest_documents():
    """
    Main function for PDF ingestion.
    Loads and splits all PDFs in DATA_DIR,
    computes embeddings, and stores them in ChromaDB.
    """
    if not os.path.isdir(DATA_DIR):
        raise FileNotFoundError(f"Data directory '{DATA_DIR}' not found. Please create it and place PDFs inside.")

    docs = []
    pdf_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(".pdf")]
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in '{DATA_DIR}'. Please add PDFs before running ingestion.")

    for filename in pdf_files:
        loader = PyPDFLoader(os.path.join(DATA_DIR, filename))
        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs_split = splitter.split_documents(docs)

    cohere_api_key = get_cohere_api_key()
    embeddings = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=cohere_api_key)
    vectordb = get_vectordb(embeddings)
    vectordb.add_documents(docs_split)
    if hasattr(vectordb, "persist"):
        vectordb.persist()
    print(f"Ingested {len(docs_split)} document chunks from {len(pdf_files)} PDFs.")

if __name__ == "__main__":
    ingest_documents()
