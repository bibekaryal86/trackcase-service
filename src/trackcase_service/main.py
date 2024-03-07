import logging
import os
import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from src.trackcase_service.api import (
    calendars,
    client,
    collections,
    court_api,
    court_case,
    filing,
    judge_api,
    ref_types,
    user_management,
    user_management_noauth,
)
from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.utils import commons, constants, logger

log = logger.Logger(logging.getLogger(__name__))


@asynccontextmanager
async def lifespan(application: FastAPI):
    commons.validate_input()
    commons.startup_app()
    yield
    commons.shutdown_app()


app = FastAPI(
    title="TrackCase Service",
    description="Backend service for processing and tracking immigration cases",
    version="1.0.1",
    lifespan=lifespan,
    openapi_url=None if commons.is_production() else "/trackcase-service/openapi.json",
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=constants.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_credentials(
    request: Request,
    http_auth_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    commons.decode_auth_credentials(request, http_auth_credentials)


app.include_router(
    court_case.router,
    dependencies=[Depends(validate_credentials)],
)
app.include_router(
    client.router,
    dependencies=[Depends(validate_credentials)],
)
app.include_router(
    filing.router,
    dependencies=[Depends(validate_credentials)],
)
app.include_router(
    collections.router,
    dependencies=[Depends(validate_credentials)],
)
app.include_router(
    calendars.router,
    dependencies=[Depends(validate_credentials)],
)
app.include_router(
    ref_types.router,
    dependencies=[Depends(validate_credentials)],
)
app.include_router(
    user_management.router,
    dependencies=[Depends(validate_credentials)],
)
app.include_router(
    user_management_noauth.router,
)
app.include_router(
    court_api.router,
    dependencies=[Depends(validate_credentials)],
)
app.include_router(
    judge_api.router,
    dependencies=[Depends(validate_credentials)],
)


@app.middleware("http")
async def log_request_response(request: Request, call_next):
    log.info(f"Receiving [ {request.method} ] URL [ {request.url} ]")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["x-process-time"] = str(process_time)
    log.info(
        f"Returning [ {request.method} ] Status Code [ {response.status_code} ] "
        f"URL [ {request.url} ] AFTER [ {format(process_time, '.4f')}ms]"
    )
    return response


@app.get("/trackcase-service/docs", include_in_schema=False)
async def custom_docs_url(
    request: Request,
):
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    return get_swagger_ui_html(openapi_url=openapi_url, title=app.title)


@app.get(
    "/trackcase-service/tests/ping/",
    tags=["Main"],
    summary="Ping Application",
)
def ping(db_session: Session = Depends(get_db_session)):
    try:
        test_database_sql = text("SELECT VERSION_NUM FROM ALEMBIC_VERSION")
        result = db_session.execute(test_database_sql)
        result_row = result.fetchone()
        if result_row:
            return {"ping": "successful", "ping_db": f"successful: {result_row[0]}"}
        else:
            return {"ping": "successful", "ping_db": "successful: no_result"}
    except OperationalError as ex:
        return {"ping": "successful", "ping_db": f"exception: {str(ex)}"}


if __name__ == "__main__":
    port = os.getenv(constants.ENV_APP_PORT, "9090")
    uvicorn.run(app, port=int(port), host="0.0.0.0", log_level=logging.WARNING)
