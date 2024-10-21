import asyncio
import logging

from fastapi import APIRouter, Depends
from typing import Annotated
from annotated_types import MaxLen
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from application.container import ApplicationContainer
from application.service.factory import ServiceFactory

from .request import SearchRequest
from .response import SearchResultResponse, SearchItemResponse

router = APIRouter()

container = ApplicationContainer(settings)
logger = logging.getLogger(__name__)


@router.post("/search", tags=["maillog"])
async def search(
        request: SearchRequest,
        connection: AsyncSession = Depends(container.get_database().get_connection)
) -> SearchResultResponse:
    search_service = ServiceFactory.get_search_service(connection)

    results = await search_service.search_by_email(request.email)

    items = [SearchItemResponse(date=result.created, log=result.str) for result in results.items]
    response = SearchResultResponse(items=items, total=results.total)

    return response
