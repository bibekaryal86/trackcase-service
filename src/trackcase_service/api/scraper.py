from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.scraper import get_court_scraper_service

router = APIRouter(prefix="/scraper", tags=["Web Scraper"])


@router.get(
    "/courts",
    status_code=HTTPStatus.OK,
)
def courts_scraper(
    request: Request,
    db_session: Session = Depends(get_db_session),
):
    get_court_scraper_service(db_session).scrape_for_courts(request)
    return {"scrape": "successful"}
