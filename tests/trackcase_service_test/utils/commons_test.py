from fastapi import FastAPI, Request

app = FastAPI()
dummy_request = Request(scope={"type": "http", "app": app})
