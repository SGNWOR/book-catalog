from src.library_catalog.api.main import BaseApiClient
from src.library_catalog.models.books import CreateBook

import httpx


class OpenLibraryClient(BaseApiClient):
    def __init__(self, url):
        super().__init__(url)

    async def get_request(self, title: str) -> dict:
        query = title.lower().replace(" ", "+")
        url = f"{self.base_url}{query}"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=url
            )
        return response.json()

    async def parse_data(self, title: str) -> dict:
        book_data = {
            'image': None,
            'description': None,
            'rating': None
        }

        data = await self.get_request(title)
        data = data["docs"][0]

        if data['cover_i']:
            book_data['image'] = f'https://covers.openlibrary.org/b/id/{data['cover_i']}.jpg'

        if data['key']:
            async with httpx.AsyncClient() as client:
                desc_data = await client.get(
                    url=f'https://openlibrary.org{data['key']}.json'
                )
                rating_data = await client.get(
                    url=f'https://openlibrary.org{data['key']}/ratings.json'
                )
            desc_data = desc_data.json()
            rating_data = rating_data.json()

            if 'description' in desc_data.keys():
                book_data['description'] = desc_data['description']

            if rating_data['summary']:
                book_data['rating'] = f'{rating_data['summary']['average']:.2f}'
        return book_data

    async def merge_info(self, title: str, book: CreateBook) -> CreateBook:
        data = await self.parse_data(title)

        book.img = data['image']
        book.desc = data['description']
        book.rating = data['rating']
        return book
