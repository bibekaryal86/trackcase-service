import os
from functools import lru_cache
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.trackcase_service.utils.constants import DB_HOST, DB_PASSWORD, DB_USERNAME

# TODO ???
os.add_dll_directory(
    "C:\\zzz_dev\\projects\\backend\\trackcase-service\\venv\\Lib\\site-packages\\clidriver\\bin"
)

db2_url = (
    f"ibm_db_sa://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}"
    f".c3n41cmd0nqnrk39u98g.databases.appdomain.cloud:30604/bludb;SECURITY=SSL;PROTOCOL=TCPIP;"
)
engine = create_engine(db2_url, pool_pre_ping=True, echo=True)


@lru_cache
def create_session() -> scoped_session:
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    return session


def get_session() -> Generator[scoped_session, None, None]:
    session = create_session()
    try:
        yield session
    finally:
        session.remove()
