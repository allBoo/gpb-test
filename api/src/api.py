from fastapi import FastAPI, Depends

from application.container import ApplicationContainer
from application.config import settings
from application.ports.api.v1 import urls as v1
# from application.ports.api.security import get_api_token_validator, setup_allowed_hosts

app = FastAPI(
    title="Maillog API",
    description="Maillog API sample",
    version="1.0.0",
    debug=settings.DEBUG,
    # dependencies=[
    #     Depends(get_api_token_validator(settings.API_TOKEN))
    # ],
)

app.include_router(v1.router)
