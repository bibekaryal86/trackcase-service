import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.trackcase_service.utils.constants import DB_HOST, DB_PASSWORD, DB_USERNAME

# TODO ???
os.add_dll_directory(
    "C:\\zzz_dev\\projects\\backend\\trackcase-service\\venv\\Lib\\site-packages\\clidriver\\bin"  # noqa: E501
)

db2_url = (
    f"ibm_db_sa://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}"
    f".c3n41cmd0nqnrk39u98g.databases.appdomain.cloud:30604"
    f"/bludb;SECURITY=SSL;PROTOCOL=TCPIP;"
)
engine = create_engine(db2_url, echo=False)  # use echo=True to show log in SysOut


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
