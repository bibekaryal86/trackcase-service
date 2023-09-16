from unittest.mock import Mock

from fastapi import FastAPI
from starlette.requests import Request

app = FastAPI()
app.mongo_client = Mock()
dummy_request = Request(scope={"type": "http", "app": app})
