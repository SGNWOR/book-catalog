from typing import Optional

from pydantic import BaseModel, Field


class CreateBook(BaseModel):
    id: int
    img: Optional[str] = None
    name: str
    author: str
    year: int
    genre: str
    desc: str
    pages: int
    rating: float
    availability: str = "available"


class UpdateBook(BaseModel):
    id: Optional[int] = Field(default=None, examples=[None])
    img: Optional[str] = Field(default=None, examples=[None])
    name: Optional[str] = Field(default=None, examples=[None])
    author: Optional[str] = Field(default=None, examples=[None])
    year: Optional[int] = Field(default=None, examples=[None])
    genre: Optional[str] = Field(default=None, examples=[None])
    desc: Optional[str] = Field(default=None, examples=[None])
    pages: Optional[int] = Field(default=None, examples=[None])
    rating: Optional[float] = Field(default=None, examples=[None])
    availability: Optional[str] = Field(default=None, examples=[None])


class SearchBook(BaseModel):
    name: Optional[str] = Field(default=None, examples=[None])
    author: Optional[str] = Field(default=None, examples=[None])
    year: Optional[int] = Field(default=None, examples=[None])
    genre: Optional[str] = Field(default=None, examples=[None])
    desc: Optional[str] = Field(default=None, examples=[None])
    pages: Optional[int] = Field(default=None, examples=[None])
    rating: Optional[float] = Field(default=None, examples=[None])
    availability: Optional[str] = Field(default=None, examples=[None])
