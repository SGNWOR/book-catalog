from httpx import AsyncClient

from src.library_catalog.api.main import BaseApiClient
from src.library_catalog.models.books import CreateBook


class OpenLibraryClient(BaseApiClient):
    def __init__(self) -> None:
        self.base_url = 'https://openlibrary.org/search.json?q='

    async def _get_request(self, title: str) -> dict:
        query = title.lower().replace(" ", "+")
        url = f"{self.base_url}{query}"

        async with AsyncClient() as client:
            response = await client.get(
                url=url
            )
        return response.json()

    async def _parse_data(self, title: str) -> dict:
        book_data = {
            'image': None,
            'description': None,
            'rating': None
        }

        data = await self._get_request(title)
        data = data["docs"][0]

        base_cover_url = 'https://covers.openlibrary.org/b/id'
        if data['cover_i']:
            data_cover_i = data['cover_i']
            book_data['image'] = f"{base_cover_url}/{data_cover_i}.jpg"

        if data['key']:
            async with AsyncClient() as client:
                data_key = data['key']
                desc_data = await client.get(
                    url=f'https://openlibrary.org{data_key}.json'
                )
                rating_data = await client.get(
                    url=f'https://openlibrary.org{data_key}/ratings.json'
                )
            desc_data = desc_data.json()
            rating_data = rating_data.json()

            if 'description' in desc_data.keys():
                book_data['description'] = desc_data['description'][0:100]

            if rating_data['summary']:
                book_rating = rating_data['summary']['average']
                book_data['rating'] = f'{book_rating:.2f}'
        return book_data

    async def add_info_from_open_library(self,
                                         title: str,
                                         book: CreateBook
                                         ) -> CreateBook:
        data = await self._parse_data(title)

        book.img = data['image']
        book.desc = data['description']
        book.rating = data['rating']
        return book
