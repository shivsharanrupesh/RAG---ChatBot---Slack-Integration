"""
FastAPI backend for IT Support Chatbot

- Exposes /ask POST endpoint for chat UI or clients.
- Accepts question and session_id, returns answer and sources.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_chain import get_rag_chain

app = FastAPI()

class QueryRequest(BaseModel):
    """Request model for /ask endpoint"""
    question: str
    session_id: str

@app.post("/ask")
def ask(request: QueryRequest):
    """
    Chatbot Q&A endpoint.
    Args:
        request (QueryRequest): Contains question and session ID.
    Returns:
        dict: Chatbot answer and document sources.
    """
    qa_chain = get_rag_chain(request.session_id)
    result = qa_chain({"question": request.question})
    return {
        "answer": result["result"],
        "sources": [
            {
                "source": doc.metadata.get("source", ""),
                "page": doc.metadata.get("page", "")
            }
            for doc in result["source_documents"]
        ]
    }
