import logging
import os
import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasicCredentials

from src.trackcase_service.utils import commons, constants, enums, logger

log = logger.Logger(logging.getLogger(__name__), __name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    commons.validate_input()
    commons.startup_db_client(application)
    yield
    commons.shutdown_db_client(application)


app = FastAPI(
    title="TrackCase Service",
    description="Backend service for processing and tracking immigration cases",
    version="1.0.1",
    lifespan=lifespan,
    openapi_url=None if commons.is_production() else "/trackcase-service/openapi.json",
    docs_url=None,
    redoc_url=None,
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
    return {"reset": "successful"}


@app.get("/trackcase-service/tests/log-level", tags=["Main"], summary="Set Log Level")
def log_level(level: enums.LogLevelOptions):
    log_level_to_set = logging.getLevelNamesMapping().get(level)
    log.set_level(log_level_to_set)
    commons.log.set_level(log_level_to_set)
    return {"set": "successful"}


@app.get("/trackcase-service/docs", include_in_schema=False)
async def custom_docs_url(
        request: Request,
        http_basic_credentials: HTTPBasicCredentials = Depends(
            constants.http_basic_security
        ),
):
    commons.validate_http_basic_credentials(request, http_basic_credentials)
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    return get_swagger_ui_html(openapi_url=openapi_url, title=app.title)


if __name__ == "__main__":
    port = os.getenv(constants.ENV_APP_PORT, "9090")
    host = "0.0.0.0"
    uvicorn.run(app, port=int(port), host="0.0.0.0", log_level=logging.WARNING)
