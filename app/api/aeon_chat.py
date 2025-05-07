# New File: aeon_chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import load_index_from_storage, StorageContext
import os

router = APIRouter()

INDEX_DIR = "storage"

class MoodInput(BaseModel):
    mood: str
    owner_id: str  # to later support personalized memory


def get_index():
    if not os.path.exists(INDEX_DIR):
        raise HTTPException(status_code=500, detail="Vector index not found.")
    ctx = StorageContext.from_defaults(persist_dir=INDEX_DIR)
    return load_index_from_storage(ctx)


@router.get("/aeon/ask")
def ask_mood():
    return {
        "question": "How is your day?",
        "options": ["happy", "sad", "angry", "tired", "motivated"]
    }


@router.post("/aeon/respond")
def respond_to_mood(input: MoodInput):
    try:
        index = get_index()
        retriever = index.as_retriever()
        engine = RetrieverQueryEngine.from_args(retriever)

        # Enrich the prompt with AI understanding and memory
        full_query = f"""
        The user said they feel {input.mood} today.
        Given past interactions and emotional tone, respond with an uplifting message.
        It can be a motivational quote or a light-hearted joke.
        """

        response = engine.query(full_query)

        return {"response": str(response)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
