from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.trackcase_service.utils.constants import DB_NAME, DB_PASSWORD, DB_USERNAME

url = (
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}"
    f"@org-{DB_NAME}-inst-trackcase-service.data-1.use1.tembo.io:5432/{DB_USERNAME}?sslmode=require"
)
engine = create_engine(url, echo=False)  # use echo=True to show log in SysOut
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
