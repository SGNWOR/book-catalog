from typing import Optional

from abc import ABC


class BaseApiClient(ABC):
    def __init__(self) -> None:
        self.base_url: str = 'url'
        self.headers: Optional[dict] = None
