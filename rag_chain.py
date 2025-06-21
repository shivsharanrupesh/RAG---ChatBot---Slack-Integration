"""
RAG Chain Factory for IT Support Chatbot

- Sets up retrieval + Cohere LLM + persistent memory
- Uses ChromaDB for document retrieval
- Uses mem0 for per-session chat history

Defines: get_rag_chain(session_id: str)
"""

import os
from langchain.vectorstores import Chroma
from langchain.embeddings import CohereEmbeddings
from langchain.llms import Cohere
from langchain.chains import ConversationalRetrievalChain
from mem0 import Memory

def get_cohere_api_key():
    """
    Fetch the Cohere API key from the environment.
    Raises:
        EnvironmentError: if key is not set.
    Returns:
        str: API key.
    """
    key = os.environ.get("COHERE_API_KEY")
    if not key:
        raise EnvironmentError("COHERE_API_KEY environment variable is not set!")
    return key

def get_vectordb(embeddings):
    """
    Return Chroma vector store for document retrieval.
    Uses persistent storage if CHROMA_DB_DIR is set, else in-memory.
    """
    chroma_db_dir = os.getenv("CHROMA_DB_DIR")
    if chroma_db_dir and os.path.isdir(chroma_db_dir):
        vectordb = Chroma(persist_directory=chroma_db_dir, embedding_function=embeddings)
    else:
        vectordb = Chroma(embedding_function=embeddings)
    return vectordb

def get_rag_chain(session_id: str):
    """
    Creates a conversational RAG chain (retriever + LLM + memory) for a session/user.
    Args:
        session_id (str): Unique session/user identifier.
    Returns:
        ConversationalRetrievalChain: The RAG pipeline.
    """
    cohere_api_key = get_cohere_api_key()
    embeddings = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=cohere_api_key)
    vectordb = get_vectordb(embeddings)
    retriever = vectordb.as_retriever()
    llm = Cohere(model="command-r-plus", cohere_api_key=cohere_api_key)
    memory = Memory(session_id=session_id, storage_path="memory_store/")  # Store history by session
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )
    return qa_chain
