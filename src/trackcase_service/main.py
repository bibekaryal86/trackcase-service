import logging
import os
import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, Header, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.trackcase_service.api import (
    case_collection_api,
    case_type_api,
    cash_collection_api,
    client_api,
    collection_method_api,
    common_api,
    court_api,
    court_case_api,
    form_api,
    form_type_api,
    hearing_calendar_api,
    hearing_type_api,
    judge_api,
    task_calendar_api,
    task_type_api,
)
from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.utils import commons, constants, logger
from src.trackcase_service.utils.commons import validate_http_basic_credentials

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


def user_name_header(
    x_user_name: str = Header(
        title="User Name in Header",
        description="To be included with every request",
    )
):
    return x_user_name


def validate_credentials(
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
):
    validate_http_basic_credentials(request, http_basic_credentials)


app.include_router(
    case_collection_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    case_type_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    cash_collection_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    client_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    collection_method_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    court_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    court_case_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    form_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    form_type_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    hearing_calendar_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    hearing_type_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    judge_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    task_calendar_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    task_type_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)
app.include_router(
    common_api.router,
    dependencies=[Depends(user_name_header), Depends(validate_credentials)],
)


@app.middleware("http")
async def log_request_response(request: Request, call_next):
    log.info(f"Receiving [ {request.method} ] URL [ {request.url} ]")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    log.info(
        f"Returning [ {request.method} ] Status Code [ {response.status_code} ] "
        f"URL [ {request.url} ] AFTER [ {format(process_time, '.4f')}ms]"
    )
    return response


@app.get("/trackcase-service/tests/ping", tags=["Main"], summary="Ping Application")
def ping():
    return {"test": "successful"}


@app.get("/trackcase-service/tests/reset", tags=["Main"], summary="Reset Cache")
def reset(request: Request):
    # TODO: placeholder to reset cache
    return {"reset": "successful"}


@app.get("/trackcase-service/tests/database", tags=["Main"], summary="Ping Database")
def test_database(
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
    db_session: Session = Depends(get_db_session),
):
    commons.validate_http_basic_credentials(request, http_basic_credentials, True)
    return commons.test_database(db_session)


@app.get("/trackcase-service/tests/log-level", tags=["Main"], summary="Set Log Level")
def log_level(level: constants.LogLevelOptions):
    log_level_to_set = logging.getLevelNamesMapping().get(level)
    log.set_level(log_level_to_set)
    commons.log.set_level(log_level_to_set)
    return {"set": "successful"}


@app.get("/trackcase-service/docs", include_in_schema=False)
async def custom_docs_url(
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
):
    commons.validate_http_basic_credentials(request, http_basic_credentials, True)
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    return get_swagger_ui_html(openapi_url=openapi_url, title=app.title)


if __name__ == "__main__":
    port = os.getenv(constants.ENV_APP_PORT, "9090")
    uvicorn.run(app, port=int(port), host="0.0.0.0", log_level=logging.WARNING)
