from abc import ABC, abstractmethod

from search.data.dto.results import SearchResults


class SearchService(ABC):
    @abstractmethod
    async def search_by_email(self, email: str) -> SearchResults:
        raise NotImplementedError
