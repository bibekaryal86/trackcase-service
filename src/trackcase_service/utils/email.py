from http import HTTPStatus

from mailjet_rest import Client
from requests import Request

from src.trackcase_service.utils import constants
from src.trackcase_service.utils.commons import raise_http_exception, read_file


class Email:
    def __init__(self):
        self.api_key = constants.MJ_PUBLIC
        self.api_secret = constants.MJ_PRIVATE
        self.api_email = constants.MJ_EMAIL

        self.mailjet = Client(auth=(self.api_key, self.api_secret), version="v3.1")

    def app_user_validation_email(self, request: Request, user_name: str):
        email_html_content = read_file("email_validate_user.html")
        activation_link = (
            "http://localhost:9090/trackcase-service/users/na/validate/email={}".format(
                user_name
            )
        )
        email_html_content = email_html_content.format(activation_link=activation_link)
        data = {
            "Messages": [
                {
                    "From": {
                        "Email": self.api_email,
                        "Name": "TrackCase Service (Activate Account)",
                    },
                    "To": [
                        {
                            "Email": user_name,
                            "Name": f"{user_name} TrackCase Service",
                        }
                    ],
                    "Subject": "TrackCase Service (Activate)",
                    "HTMLPart": email_html_content,
                }
            ]
        }
        result = self.mailjet.send.create(data=data)

        result_messages = result.get("Messages", {})
        if (
            result_messages
            and len(result_messages) > 0
            and result_messages[0].get("Success") == "success"
        ):
            pass
        else:
            raise_http_exception(
                request=request, sts_code=HTTPStatus.UNPROCESSABLE_ENTITY
            )


def get_email_service() -> Email:
    return Email()
