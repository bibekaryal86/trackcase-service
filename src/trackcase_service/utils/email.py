from http import HTTPStatus

from fastapi import Request
from mailjet_rest import Client

from src.trackcase_service.utils import constants
from src.trackcase_service.utils.commons import raise_http_exception, read_file, encode_email_address


class Email:
    def __init__(self):
        self.api_key = constants.MJ_PUBLIC
        self.api_secret = constants.MJ_PRIVATE
        self.api_email = constants.MJ_EMAIL

        self.mailjet = Client(auth=(self.api_key, self.api_secret), version="v3.1")

    def app_user_validation_email(self, request: Request, user_name: str):
        email_html_content = read_file("email_validate_user.html")
        activation_link = "{}}/trackcase-service/users/na/validate/email={}".format(
            request.base_url, encode_email_address(user_name, 15)
        )
        email_html_content = email_html_content.format(activation_link=activation_link)
        data = {
            "Messages": [
                {
                    "From": {
                        "Email": self.api_email,
                        "Name": f"TrackCase Service {self.api_email}",
                    },
                    "To": [
                        {
                            "Email": user_name,
                            "Name": f"TrackCase Service {user_name}",
                        }
                    ],
                    "Subject": "TrackCase Service (Activate)",
                    "HTMLPart": email_html_content,
                }
            ]
        }
        result = self.mailjet.send.create(data=data)
        if result.status_code != HTTPStatus.OK:
            raise_http_exception(
                request=request,
                sts_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                error="Failure to send validation email",
            )


def get_email_service() -> Email:
    return Email()
