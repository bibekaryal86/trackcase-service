from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.trackcase_service.utils.constants import DB_NAME, DB_PASSWORD, DB_USERNAME

url = (
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}"
    f"@{DB_NAME}.db.elephantsql.com/{DB_USERNAME}"
)
engine = create_engine(url, echo=False)  # use echo=True to show log in SysOut
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
