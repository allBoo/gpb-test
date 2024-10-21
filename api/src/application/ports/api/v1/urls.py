from fastapi import APIRouter
from .maillog import urls as maillog  # type: ignore

router = APIRouter(
    prefix='/v1'
)
router.include_router(maillog.router)
