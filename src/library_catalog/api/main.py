from typing import Optional

from abc import ABC, abstractmethod


class BaseApiClient(ABC):
    def __init__(self, url, headers: Optional[dict] = None):
        self.base_url = url
        self.headers = headers

    @abstractmethod
    def get_request(self):
        pass
