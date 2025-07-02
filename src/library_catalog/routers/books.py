from fastapi import APIRouter, Depends


from src.library_catalog.models.books import CreateBook, SearchBook
from src.library_catalog.api.book_repository import BookRepository


db = BookRepository(
    "https://api.jsonbin.io/v3/b/680a6d6f8561e97a5006babf",
    {
        "Content-Type": "application/json",
        "X-Master-Key": "$2a$10$lPrsM6IMpw8D0PDQcnGT5ukGheZBJ4b0nCtRSQ/kOsgKpzR6iMoIG"
        }
)

router = APIRouter(prefix='/books', tags=['books'])


@router.get('/')
async def get_books(filter: SearchBook = Depends()):
    return await db.get_filtered(filter)


@router.get('/{id}')
async def get_book(id: int):
    return await db.get_by_id(id)


@router.post('/book')
async def add_book(book: CreateBook):
    return await db.post_request(book)


@router.put('/detail/{id}')
async def update_book(id: int, book: CreateBook):
    return await db.update_request(book, id)


@router.delete('/delete')
async def delete_book(id: int):
    return await db.delete_request(id)
