from fastapi import APIRouter

from src.library_catalog.models.books import CreateBook, SearchBook, UpdateBook
from src.library_catalog.api.book_repository import JsonBinClient


db = JsonBinClient()

router = APIRouter(prefix='/books', tags=['books'])


@router.put('/')
async def get_books_by_parameters(filter: SearchBook):
    return await db.get_filtered(filter)


@router.get('/{id}')
async def get_book_by_id(id: int):
    return await db.get_by_id(id)


@router.post('/')
async def create_book(book: CreateBook):
    return await db.post_request(book)


@router.put('/update/{id}')
async def update_book(id: int, book: UpdateBook):
    return await db.update_request(book, id)


@router.delete('/delete')
async def delete_book(id: int):
    return await db.delete_request(id)
