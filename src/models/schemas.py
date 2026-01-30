from pydantic import BaseModel


class DocumentCreate(BaseModel):
    id: int
    title: str
    content: str
    category: str | None = None



class DocumentUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    category: str | None = None


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


class FilterSearchRequest(BaseModel):
    query: str
    limit: int = 5
    category: str
