import requests
from bs4 import BeautifulSoup
from fastapi import Request
from sqlalchemy.orm import Session


class Scraper:
    def __init__(self, url_to_scrape: str):
        self.url_to_scrape = url_to_scrape

    def scrape(self):
        response = requests.get(self.url_to_scrape)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
        else:
            raise RuntimeError(f'Invalid Response code of {response.status_code} scraping url: {self.url_to_scrape}')


class CourtScraper:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def scrape_for_courts(self, request: Request):
        print(self.db_session.is_active, request.state)        # TODO remove this line
        url = 'https://www.justice.gov/eoir/immigration-court-operational-status'
        scraper = Scraper(url_to_scrape=url)
        scraper.scrape()


def get_court_scraper_service(db_session: Session) -> CourtScraper:
    return CourtScraper(db_session)
