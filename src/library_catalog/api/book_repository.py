from src.library_catalog.api.main import BaseApiClient
from src.library_catalog.api.open_library_client import OpenLibraryClient
from src.library_catalog.models.books import CreateBook, SearchBook

import httpx

from fastapi.encoders import jsonable_encoder


open_library_client = OpenLibraryClient(
    'https://openlibrary.org/search.json?q='
    )


class BookRepository(BaseApiClient):
    def __init__(self, url, headers) -> None:
        super().__init__(url, headers)

    async def get_request(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=self.base_url,
                headers=self.headers
                )
        return response.json().get("record", {})

    async def post_request(self, book: CreateBook) -> dict:
        current_data = await self.get_request()
        book = await open_library_client.merge_info(book.name, book)

        book.id = len(current_data) + 1

        async with httpx.AsyncClient() as client:
            response = await client.put(
                url=self.base_url,
                json=current_data + [jsonable_encoder(book)],
                headers=self.headers
            )
        return response.json()

    async def get_by_id(self, id: int) -> dict:
        current_data = await self.get_request()
        return current_data[id-1]

    async def update_request(self, book: CreateBook, id: int) -> dict:
        current_data = await self.get_request()
        book.id = id
        current_data[id-1] = jsonable_encoder(book)
        async with httpx.AsyncClient() as client:
            response = await client.put(
                url=self.base_url,
                json=current_data,
                headers=self.headers
            )
        return response.json()

    async def delete_request(self, id: int) -> dict:
        current_data = await self.get_request()
        current_data.pop(id-1)
        index = 0
        for i in range(0, len(current_data)):
            index += 1
            current_data[i]['id'] = index
        async with httpx.AsyncClient() as client:
            response = await client.put(
                url=self.base_url,
                json=current_data,
                headers=self.headers
            )
        return response.json()

    async def get_filtered(self, filter: SearchBook) -> list[dict | None]:
        books_data = await self.get_request()

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
        if filter.availability:
            books_data = [
                b for b in books_data
                if filter.availability.lower() == b['availability'].lower()
                ]

        return books_data
