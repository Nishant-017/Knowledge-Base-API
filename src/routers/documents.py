from fastapi import APIRouter , HTTPException


from src.services.embedding_service import EmbeddingGenerator
from src.services.qdrant_service import QdrantService
from src.models.schemas import DocumentCreate
from src.models.schemas import SearchRequest
from src.models.schemas import FilterSearchRequest

router = APIRouter(tags=["documents"])

# create services (single instances)
embedder = EmbeddingGenerator()
qdrant = QdrantService()

COLLECTION_NAME = "kb_embedded"


@router.post("/documents")
def create_document(doc: DocumentCreate):
    # 1) get embedding dimension & ensure collection exists
    dims = embedder.get_dimensions()
    qdrant.ensure_collection(COLLECTION_NAME, dims)

    # 2) generate embedding for content
    vector = embedder.embed_single(doc.content)

    # 3) prepare payload
    payload = {
        "title": doc.title,
        "content": doc.content,
        "category": doc.category
    }

    # 4) store in Qdrant
    qdrant.add_document(
        collection_name=COLLECTION_NAME,
        doc_id=doc.id,
        vector=vector,
        payload=payload
    )

    return {"status": "success", "message": "Document stored successfully"}




@router.post("/search")
def search_documents(request: SearchRequest):
    #  generate embedding for query
    query_vector = embedder.embed_single(request.query)

    #  search in Qdrant
    results = qdrant.search_documents(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=request.limit
    )

    #  format response
    formatted = []

    for r in results:
        formatted.append({
            "id": r.id,
            "score": r.score,
            "payload": r.payload
        })

    return {"results": formatted}

    

@router.get("/collections")
def list_collections():
    collections=qdrant.list_collections()
    return {"collections":collections}


@router.delete("/collections/{collection_name}")
def delete_collection(collection_name:str):

    if collection_name not in qdrant.list_collections():
        raise HTTPException(
            status_code=404,
            detail=f"Collection {collection_name} not found"
        )
    
    qdrant.delete_collection(collection_name)
    return{"status":"success",
           "message":f"{collection_name} deleted successfully" }


@router.get("/documents/{id}")
def get_documents(id:int):

    results=qdrant.list_documents(
        collection_name=COLLECTION_NAME
    )
    
    for r in results:
        if r.id==id:
            return {
                "id":r.id,
                "payload":r.payload
            }
    raise HTTPException (
        status_code=404,
        detail=f"Document with id {id} not found"
        )


@router.delete("/documents/{id}")
def delete_document(id:int):

    results=qdrant.list_documents(
        collection_name=COLLECTION_NAME
    )
    
    for r in results:
        if r.id==id:
            qdrant.client.delete(
                collection_name=COLLECTION_NAME,
                points_selector=[r.id]
            )
            return{"status":"success",
                   "message":f"Document with id {id} deleted successfully"}
    raise HTTPException(
        status_code=404,
        detail=f"Document with id {id} not found"
    )


@router.put("/documents/{id}")
def update_document(id:int,doc:DocumentCreate):
    results=qdrant.list_documents(
        collection_name=COLLECTION_NAME
    )
    for r in results:
        if r.id==id:
            # generate new embedding
            vector=embedder.embed_single(doc.content)
            # prepare new payload
            payload={
                "title":doc.title,
                "content":doc.content,
                "category":doc.category
            }
            # update document
            qdrant.add_document(
                collection_name=COLLECTION_NAME,
                doc_id=id,
                vector=vector,
                payload=payload
            )
            return{"status":"success",
                   "message":f"Document with id {id} updated successfully"}


@router.post("/collections")
def create_collection(collection_name:str,vector_size:int):
    existing = qdrant.list_collections()

    if collection_name in existing:
        raise HTTPException(
            status_code=409,
            detail=f"Collection {collection_name} already exists"
        )

    qdrant.ensure_collection(collection_name,vector_size)
    return{"status":"success",
           "message":f"Collection {collection_name} created successfully"}




@router.get("/list_all")
def list_documents(limit: int = 10, offset: int = 0):
    result = qdrant.list_documents_paginated(
        collection_name=COLLECTION_NAME,
        limit=limit,
        offset=offset
    )

    formatted = []

    for r in result["points"]:
        formatted.append({
            "id": r.id,
            "payload": r.payload
        })

    return {
        "documents": formatted,
        "next_offset": result["next_offset"]
    }




@router.post("/search/filter")
def filtered_search(request: FilterSearchRequest):
    query_vector = embedder.embed_single(request.query)

    results = qdrant.search_documents_with_filter(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=request.limit,
        category=request.category,
    )

    formatted = []

    for r in results:
        formatted.append({
            "id": r.id,
            "score": r.score,
            "payload": r.payload
        })

    return {"results": formatted}

@router.get("/stats")
def get_stats():

    
    total = qdrant.client.count(
        collection_name=COLLECTION_NAME,
        exact=True
    ).count

    
    vector_dimension = embedder.get_dimensions()

    
    docs = qdrant.list_documents(collection_name=COLLECTION_NAME)

    category_counts = {}

    for d in docs:
        category = d.payload.get("category", "unknown")

        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    
    return {
        "collection": COLLECTION_NAME,
        "total_documents": total,
        "vector_dimension": vector_dimension,
        "categories": category_counts
    }
