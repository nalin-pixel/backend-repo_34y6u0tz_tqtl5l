import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import create_document, get_documents, db
from schemas import Note, Message

app = FastAPI(title="Rural Education Helper API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Rural Education Helper API is running"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Helper to convert ObjectId to str

def serialize(doc: dict):
    if not doc:
        return doc
    d = dict(doc)
    if "_id" in d:
        d["id"] = str(d.pop("_id"))
    return d

# Notes endpoints
@app.post("/api/notes")
def add_note(note: Note):
    try:
        note_id = create_document("note", note)
        return {"id": note_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notes")
def list_notes(subject: Optional[str] = None, grade: Optional[str] = None):
    try:
        filters = {}
        if subject:
            filters["subject"] = subject
        if grade:
            filters["grade"] = grade
        docs = get_documents("note", filters or {}, limit=100)
        return [serialize(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Messages endpoints
@app.post("/api/messages")
def send_message(msg: Message):
    try:
        msg_id = create_document("message", msg)
        return {"id": msg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/messages")
def list_messages(limit: int = 50):
    try:
        docs = get_documents("message", {}, limit=limit)
        return [serialize(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
