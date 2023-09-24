import logging
import os
import time
from contextlib import asynccontextmanager

import api.case_collection_api as case_collection_api
import api.case_type_api as case_type_api
import api.cash_collection_api as cash_collection_api
import api.client_api as client_api
import api.collection_method_api as collection_method_api
import api.court_api as court_api
import api.court_case_api as court_case_api
import api.form_api as form_api
import api.form_status_api as form_status_api
import api.form_type_api as form_type_api
import api.hearing_calendar_api as hearing_calendar_api
import api.hearing_type_api as hearing_type_api
import api.history_form_api as history_form_api
import api.judge_api as judge_api
import api.task_calendar_api as task_calendar_api
import api.task_type_api as task_type_api
import uvicorn
from fastapi import Depends, FastAPI, Header, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session
from utils import commons, constants, enums, logger

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


def user_name_header(
    usernameheader: str = Header(
        title="User Name in Header",
        description="To be included with every request",
        convert_underscores=False,
    )
):
    return usernameheader


app.include_router(case_type_api.router, dependencies=[Depends(user_name_header)])
app.include_router(case_collection_api.router, dependencies=[Depends(user_name_header)])
app.include_router(cash_collection_api.router, dependencies=[Depends(user_name_header)])
app.include_router(client_api.router, dependencies=[Depends(user_name_header)])
app.include_router(
    collection_method_api.router, dependencies=[Depends(user_name_header)]
)
app.include_router(court_api.router, dependencies=[Depends(user_name_header)])
app.include_router(court_case_api.router, dependencies=[Depends(user_name_header)])
app.include_router(form_api.router, dependencies=[Depends(user_name_header)])
app.include_router(form_status_api.router, dependencies=[Depends(user_name_header)])
app.include_router(form_type_api.router, dependencies=[Depends(user_name_header)])
app.include_router(
    hearing_calendar_api.router, dependencies=[Depends(user_name_header)]
)
app.include_router(hearing_type_api.router, dependencies=[Depends(user_name_header)])
app.include_router(history_form_api.router, dependencies=[Depends(user_name_header)])
app.include_router(judge_api.router, dependencies=[Depends(user_name_header)])
app.include_router(task_calendar_api.router, dependencies=[Depends(user_name_header)])
app.include_router(task_type_api.router, dependencies=[Depends(user_name_header)])


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


@app.get("/trackcase-service/tests/reorg", tags=["Main"], summary="Reset Reorg Tables")
def reorg(
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(
        constants.http_basic_security
    ),
    db_session: Session = Depends(commons.get_db_session),
):
    commons.validate_http_basic_credentials(request, http_basic_credentials, True)
    commons.reorg_tables(db_session)
    return {"reorg": "successful"}


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
    commons.validate_http_basic_credentials(request, http_basic_credentials, True)
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    return get_swagger_ui_html(openapi_url=openapi_url, title=app.title)


if __name__ == "__main__":
    port = os.getenv(constants.ENV_APP_PORT, "9090")
    host = "0.0.0.0"
    uvicorn.run(app, port=int(port), host="0.0.0.0", log_level=logging.WARNING)
