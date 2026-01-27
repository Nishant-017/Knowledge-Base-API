from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct



class QdrantService:

    def __init__(self, path: str = "./qdrant_data"):
        self.client = QdrantClient(path=path)

    def ensure_collection(self, collection_name: str, vector_size: int) -> None:
    #create collection if not exists

        existing = [c.name for c in self.client.get_collections().collections]

        if collection_name in existing:
            return

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

    def add_document(self,collection_name: str,doc_id: int, vector: list[float], payload: dict) -> None:
   

        point = PointStruct(
            id=doc_id,
            vector=vector,
            payload=payload
        )
        self.client.upsert(
            collection_name=collection_name,
            points=[point]
        )


    def search_documents(self, collection_name: str, query_vector: list[float], limit: int = 5):
        
        results = self.client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
        with_payload=True
    )

        return results.points
    


    
    def list_documents(self, collection_name: str):
        points, _ = self.client.scroll(
            collection_name=collection_name,
            limit=1000,
            with_payload=True,
            with_vectors=False
    )
        return points

    

    def list_collections(self)-> list[str]:

        existing = [c.name for c in self.client.get_collections().collections]
        return existing 
    
    
    def delete_collection(self,collection_name:str) -> None:
        self.client.delete_collection(collection_name=collection_name)



    def list_documents_paginated(
        self,
        collection_name: str,
        limit: int = 10,
        offset: int = 0
        ):
        points, next_offset = self.client.scroll(
            collection_name=collection_name,
            limit=limit,
            offset=offset,
            with_payload=True,
            with_vectors=False
        )
        return {
            "points": points,
            "next_offset": next_offset
        }