import csv

import requests
from bs4 import BeautifulSoup
from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.service import schemas
from src.trackcase_service.service.court import get_court_service
from src.trackcase_service.service.ref_types import get_ref_types_service


def get_component_status_map(
    db_session: Session, request: Request, component_name: schemas.ComponentStatusNames
):
    court_status_list = get_ref_types_service(
        service_type=schemas.RefTypesServiceRegistry.COMPONENT_STATUS,
        db_session=db_session,
    ).get_component_status(
        request,
        component_name,
    )
    if court_status_list:
        return {status.status_name: status.id for status in court_status_list}

    raise RuntimeError(f"No Component Status for {component_name}")


def create_csv(file_name, csv_data):
    fieldnames = list(csv_data[0].keys())
    with open(file_name, "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in csv_data:
            writer.writerow(data)


class Scraper:
    def __init__(self, url_to_scrape: str):
        self.url_to_scrape = url_to_scrape

    def scrape(self):
        response = requests.get(self.url_to_scrape)

        if response.status_code == 200:
            return BeautifulSoup(response.content, "html.parser")
        else:
            raise RuntimeError(
                f"Invalid Response code of {response.status_code} scraping url: {self.url_to_scrape}"
            )


def extract_court_table(court_table_row, court_statuses):
    court_name = court_table_row.find("td", class_="views-field-nothing")
    name = court_name.find("a").text.strip() + " Immigration Court"
    court_url = court_name.find("a")["href"]

    # Extract address information from the nested <p> tag
    address_data = court_name.find("p", class_="address")
    street_address = ", ".join(
        [
            line.text.strip()
            for line in address_data.find_all(
                "span",
                class_=lambda class_: class_ in ["address-line1", "address-line2"],
            )
        ]
    )
    city = address_data.find("span", class_="locality").text.strip()
    state = address_data.find("span", class_="administrative-area").text.strip()
    zip_code = address_data.find("span", class_="postal-code").text.strip()
    court_status_str = court_table_row.find(
        "td", class_="views-field-field-eoir-court-status"
    ).text.strip()
    court_status = court_statuses.get(court_status_str)

    if court_status is None:
        if court_status_str.startswith("OPEN"):
            court_status = court_statuses.get("OPEN")
        elif court_status_str.startswith("CLOSED"):
            court_status = court_statuses.get("CLOSED")

    return schemas.CourtRequest(
        name=name,
        court_url=court_url,
        component_status_id=court_status,
        street_address=street_address,
        city=city,
        state=state,
        zip_code=zip_code,
    )


# does not have phone number or dhs address data
class CourtScraper:
    def __init__(self, db_session: Session, request: Request):
        self.db_session = db_session
        self.request = request

    def scrape_for_courts(self):
        court_statuses = get_component_status_map(
            self.db_session, self.request, schemas.ComponentStatusNames.COURTS
        )
        url = "https://www.justice.gov/eoir/immigration-court-operational-status"
        soup = Scraper(url_to_scrape=url).scrape()
        court_table = soup.find("table", class_="usa-table")

        if court_table:
            # Extract table data
            courts_data = []
            # skip header (index 0) and begin with 1st data row (index 1):
            for row in court_table.find_all("tr")[1:]:
                courts_data.append(extract_court_table(row, court_statuses))

    def insert_court_data(self, court_requests):
        successes = []
        failures = []
        for court_request in court_requests:
            try:
                get_court_service(db_session=self.db_session).create_court(
                    self.request, court_request
                )
                successes.append(court_request)
            except Exception as ex:
                failures.append({"court_request": court_request, "error": str(ex)})
        self.create_csv_data(successes, True)
        self.create_csv_data(failures, False)

    @staticmethod
    def create_csv_data(successes_or_failures, is_success):
        csv_data = []
        for success_or_failure in successes_or_failures:
            csv_data.append(
                {
                    "name": success_or_failure.name,
                    "court_url": success_or_failure.court_url,
                    "component_status_id": success_or_failure.component_status_id,
                    "street_address": success_or_failure.street_address,
                    "city": success_or_failure.city,
                    "state": success_or_failure.state,
                    "zip_code": success_or_failure.zip_code,
                }
            )
        if len(csv_data) > 0:
            if is_success:
                create_csv(f"courts_import_successes.csv", csv_data)
            else:
                create_csv(f"courts_import_failures.csv", csv_data)
        else:
            print("NO CSV DATA")


def get_court_scraper_service(db_session: Session, request: Request) -> CourtScraper:
    return CourtScraper(db_session, request)
