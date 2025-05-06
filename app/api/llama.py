from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.query_engine import RetrieverQueryEngine
import os

router = APIRouter()

INDEX_DIR = "storage"
index = None  # Cached in memory


# ---------- Helper ----------
def get_or_load_index():
    global index
    if index is None:
        if os.path.exists(INDEX_DIR):
            storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
            index = load_index_from_storage(storage_context)
        else:
            raise ValueError("No index found. Please add documents first.")
    return index


# ---------- Models ----------
class DocumentInput(BaseModel):
    content: str


class QueryInput(BaseModel):
    query: str


class DeleteInput(BaseModel):
    doc_id: str


# ---------- Routes ----------


@router.post("/update-index")
def update_index(doc: DocumentInput):
    global index

    os.makedirs("tmp_docs", exist_ok=True)
    file_path = "tmp_docs/temp_doc.txt"
    with open(file_path, "w") as f:
        f.write(doc.content)

    try:
        new_docs = SimpleDirectoryReader("tmp_docs").load_data()

        if os.path.exists(INDEX_DIR):
            storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
            index = load_index_from_storage(storage_context)
        else:
            index = VectorStoreIndex.from_documents(new_docs)

        index.insert_documents(new_docs)
        index.storage_context.persist(persist_dir=INDEX_DIR)

        return {"message": "Index updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query-index")
def query_index(q: QueryInput):
    try:
        index = get_or_load_index()
        engine = RetrieverQueryEngine.from_args(index.as_retriever())
        response = engine.query(q.query)
        return {"response": str(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/delete-document")
def delete_document(delete_input: DeleteInput):
    try:
        index = get_or_load_index()

        # Delete by document ID
        index.delete_ref_doc(delete_input.doc_id)
        index.storage_context.persist(persist_dir=INDEX_DIR)

        return {"message": f"Document {delete_input.doc_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
