import csv
import logging

import requests
from bs4 import BeautifulSoup
from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.service import schemas
from src.trackcase_service.service.court import get_court_service
from src.trackcase_service.service.judge import get_judge_service
from src.trackcase_service.service.ref_types import get_ref_types_service
from src.trackcase_service.utils import logger

log = logger.Logger(logging.getLogger(__name__))


def create_csv(file_name, csv_data):
    fieldnames = list(csv_data[0].keys())
    with open(file_name, "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in csv_data:
            writer.writerow(data)


def get_component_status_map(
    db_session: Session, request: Request, component_name: schemas.ComponentStatusNames
):
    component_statuses = get_ref_types_service(
        service_type=schemas.RefTypesServiceRegistry.COMPONENT_STATUS,
        db_session=db_session,
    ).get_component_status(
        request,
        component_name,
    )
    if component_statuses:
        return {status.status_name: status.id for status in component_statuses}
    raise RuntimeError(f"Component Status not Found for {component_name}!")


def get_judges_active_status(
    db_session: Session,
    request: Request,
):
    judge_active_status = get_component_status_map(
        db_session, request, schemas.ComponentStatusNames.JUDGES
    ).get("ACTIVE")
    if judge_active_status:
        return judge_active_status
    raise RuntimeError("Judge Active Status not Found!")


def get_courts_map(db_session: Session, request: Request):
    courts = get_court_service(db_session).read_court(request).data
    if courts:
        return {court.name: court.id for court in courts}
    raise RuntimeError("Courts List Not Found!")


def get_court_status(court_status_str, court_statuses):
    court_status = None
    if court_status_str.startswith("OPEN"):
        court_status = court_statuses.get("OPEN")
    elif court_status_str.startswith("CLOSED"):
        court_status = court_statuses.get("CLOSED")
    elif "OPEN" in court_status_str:
        court_status = court_statuses.get("OPEN")
    elif "CLOSED" in court_status_str:
        court_status = court_statuses.get("CLOSED")
    return court_status


def extract_court_details(court_table_row, court_statuses):
    court_name = court_table_row.find("td", class_="views-field-nothing")
    if court_name:
        name = court_name.find("a")
        if name:
            name = name.text.strip() + " Immigration Court"
            court_url = court_name.find("a")["href"]

            address_data = court_name.find("p", class_="address")
            street_address = ", ".join(
                [
                    line.text.strip()
                    for line in address_data.find_all(
                        "span",
                        class_=lambda class_: class_
                        in ["address-line1", "address-line2"],
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
                court_status = get_court_status(court_status_str, court_statuses)

            if court_status is None:
                log.error(msg="Court Status is None", extra=court_name)
                return None
            else:
                return schemas.CourtRequest(
                    name=name,
                    court_url=court_url,
                    component_status_id=court_status,
                    street_address=street_address,
                    city=city,
                    state=state,
                    zip_code=zip_code,
                )
    return None


def extract_judge_details(court_tag, courts_map, judge_status):
    court_name = court_tag.text.strip()
    judge_table = court_tag.find_next_sibling("table")
    rows = judge_table.find_all("tr")[1:]

    for row in rows:
        cells = row.find_all("td")
        if cells:
            name = cells[0].text.strip()
            webex = cells[1].find("a")["href"]
            # access_code = cells[2].text.strip()
            court_id = courts_map.get(court_name.upper())
            return schemas.JudgeRequest(
                name=name,
                webex=webex,
                court_id=court_id,
                component_status_id=judge_status,
            )
    return None


class WebScraper:
    def __init__(self, url_to_scrape: str):
        self.url_to_scrape = url_to_scrape

    def scrape(self):
        response = requests.get(self.url_to_scrape)

        if response.status_code == 200:
            return BeautifulSoup(response.content, "html.parser")
        else:
            raise RuntimeError(
                f"Invalid Response code of {response.status_code} scraping url: {self.url_to_scrape}"  # noqa: E501
            )


# does not have phone number or dhs address data
class CourtsImport:
    def __init__(self, db_session: Session, request: Request):
        self.db_session = db_session
        self.request = request

    def import_courts(self):
        court_statuses = get_component_status_map(
            self.db_session, self.request, schemas.ComponentStatusNames.COURTS
        )
        url = "https://www.justice.gov/eoir/immigration-court-operational-status"
        soup = WebScraper(url_to_scrape=url).scrape()
        court_table = soup.find("table", class_="usa-table")
        courts_data = []

        if court_table:
            # skip header (index 0) and begin with 1st data row (index 1):
            for row in court_table.find_all("tr")[1:]:
                court = extract_court_details(row, court_statuses)
                if court:
                    courts_data.append(court)
                else:
                    log.error(msg="Court is None", extra=row)
        self.insert_court_data(courts_data)

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
                log.error(msg="Error Inserting Court", extra=ex)
                failures.append(court_request)
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
                create_csv("courts_import_successes.csv", csv_data)
            else:
                create_csv("courts_import_failures.csv", csv_data)
        else:
            log.info("COURTS IMPORT NO CSV DATA")


class JudgesImport:
    def __init__(self, db_session: Session, request: Request):
        self.db_session = db_session
        self.request = request

    def import_judges(self):
        judge_active_status = get_judges_active_status(self.db_session, self.request)
        courts_map = get_courts_map(self.db_session, self.request)

        judges_data = []
        url = "https://www.justice.gov/eoir/find-immigration-court-and-access-internet-based-hearings"  # noqa: E501
        soup = WebScraper(url_to_scrape=url).scrape()

        court_tags = soup.find_all("h3")
        for court_tag in court_tags:
            judge = extract_judge_details(court_tag, courts_map, judge_active_status)
            if judge:
                judges_data.append(judge)
            else:
                log.error(msg="Court is None", extra=court_tag)
        self.insert_judge_data(judges_data)

    def insert_judge_data(self, judge_requests):
        successes = []
        failures = []
        for judge_request in judge_requests:
            try:
                get_judge_service(db_session=self.db_session).create_judge(
                    self.request, judge_request
                )
                successes.append(judge_request)
            except Exception as ex:
                log.error(msg="Error Inserting Judge", extra=ex)
                failures.append(judge_request)
        self.create_csv_data(successes, True)
        self.create_csv_data(failures, False)

    @staticmethod
    def create_csv_data(successes_or_failures, is_success):
        csv_data = []
        for success_or_failure in successes_or_failures:
            csv_data.append(
                {
                    "name": success_or_failure.name,
                    "webex": success_or_failure.webex,
                    "component_status_id": success_or_failure.component_status_id,
                    "court_id": success_or_failure.court_id,
                }
            )
        if len(csv_data) > 0:
            if is_success:
                create_csv("judges_import_successes.csv", csv_data)
            else:
                create_csv("judges_import_failures.csv", csv_data)
        else:
            log.info("JUDGES IMPORT NO CSV DATA")


def get_courts_import_service(db_session: Session, request: Request) -> CourtsImport:
    return CourtsImport(db_session, request)


def get_judges_import_service(db_session: Session, request: Request) -> JudgesImport:
    return JudgesImport(db_session, request)
