from typing import Union

from httpx import AsyncClient

from fastapi.encoders import jsonable_encoder

from src.library_catalog.api.main import BaseApiClient
from src.library_catalog.api.open_library_client import OpenLibraryClient

from src.library_catalog.models.books import CreateBook, SearchBook, UpdateBook


class JsonBinClient(BaseApiClient):
    def __init__(self) -> None:
        self.base_url = "https://api.jsonbin.io/v3/b/680a6d6f8561e97a5006babf"
        self.api_key = "$2a$10$lPrsM6IMpw8D0PDQcnGT5ukGheZBJ4b0nCtRSQ"
        self.headers = {
            "Content-Type": "application/json",
            "X-Master-Key": f'{self.api_key}/kOsgKpzR6iMoIG'
            }

    async def _get_request(self) -> list[dict]:
        async with AsyncClient() as client:
            response = await client.get(
                url=self.base_url,
                headers=self.headers
                )
        return response.json().get("record", {})

    async def post_request(self, book: CreateBook) -> dict:
        open_library_client = OpenLibraryClient()

        current_data = await self._get_request()

        book = await open_library_client.add_info_from_open_library(book.name,
                                                                    book)
        book.id = len(current_data) + 1

        async with AsyncClient() as client:
            response = await client.put(
                url=self.base_url,
                json=current_data + [jsonable_encoder(book)],
                headers=self.headers
            )
        return response.json()

    async def get_by_id(self, id: int) -> dict:
        current_data = await self._get_request()
        return current_data[id-1]

    async def update_request(self, book: UpdateBook, id: int) -> dict:
        current_data = await self._get_request()

        current_book = await self.get_by_id(id)

        book.id = id

        if book.img is None:
            book.img = current_book['img']

        if book.name is None:
            book.name = current_book['name']

        if book.author is None:
            book.author = current_book['author']

        if book.year is None:
            book.year = current_book['year']

        if book.genre is None:
            book.genre = current_book['genre']

        if book.desc is None:
            book.desc = current_book['desc']

        if book.pages is None:
            book.pages = current_book['pages']

        if book.rating is None:
            book.rating = current_book['rating']

        if book.availability is None:
            book.availability = current_book['availability']

        current_data[id-1] = jsonable_encoder(book)

        async with AsyncClient() as client:
            response = await client.put(
                url=self.base_url,
                json=current_data,
                headers=self.headers
            )
        return response.json()

    async def delete_request(self, id: int) -> dict:
        current_data = await self._get_request()

        current_data.pop(id-1)

        index = 0
        for i in range(0, len(current_data)):
            index += 1
            current_data[i]['id'] = index

        async with AsyncClient() as client:
            response = await client.put(
                url=self.base_url,
                json=current_data,
                headers=self.headers
            )
        return response.json()

    async def get_filtered(self, filter: SearchBook
                           ) -> list[Union[dict, None]]:

        books_data = await self._get_request()

        if filter.name:
            books_data = [
                b for b in books_data
                if filter.name.lower() in b['name'].lower()
                ]
        if filter.author:
            books_data = [
                b for b in books_data
                if filter.author.lower() in b['author'].lower()
                ]
        if filter.year:
            books_data = [
                b for b in books_data
                if filter.year in b['year']
                ]
        if filter.genre:
            books_data = [
                b for b in books_data
                if filter.genre.lower() in b['genre'].lower()
                ]
        if filter.desc:
            books_data = [
                b for b in books_data
                if filter.desc.lower() in b['desc'].lower()
                ]
        if filter.pages:
            books_data = [
                b for b in books_data
                if f'{filter.pages}' in str(b['pages'])
                ]
        if filter.rating:
            books_data = [
                b for b in books_data
                if f'{filter.rating}' in b['rating'].lower()
                ]
        if filter.availability:
            books_data = [
                b for b in books_data
                if filter.availability.lower() == b['availability'].lower()
                ]

        return books_data
