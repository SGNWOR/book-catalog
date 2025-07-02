from pydantic import BaseModel

from typing import Optional


class CreateBook(BaseModel):
    id: int
    img: str | None = None
    name: str
    author: str
    year: int
    genre: str
    desc: str
    pages: int
    rating: float
    availability: str = "available"


class SearchBook(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    availability: Optional[str] = None
