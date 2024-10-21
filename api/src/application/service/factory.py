from sqlalchemy.ext.asyncio import AsyncSession

from search.service import SearchService
from search.service.database import DatabaseSearchService


class ServiceFactory:

    @staticmethod
    def get_search_service(connection: AsyncSession) -> SearchService:
        return DatabaseSearchService(connection)
