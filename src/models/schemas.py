from pydantic import BaseModel


class DocumentCreate(BaseModel):
    id: int
    title: str
    content: str
    category: str | None = None


class SearchRequest(BaseModel):
    query: str
    limit: int = 5
