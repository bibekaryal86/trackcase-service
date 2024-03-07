import unittest
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from src.trackcase_service.main import app, get_db_session


class MainTest(unittest.TestCase):

    def test_ping(self):
        mock_session = MagicMock()
        app.dependency_overrides[get_db_session] = mock_session

        client = TestClient(app)
        response = client.get("/trackcase-service/tests/ping/?args=value&kwargs=value")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("ping"), "successful")
        self.assertIsNotNone(response.json().get("ping_db"))
        # self.assertEqual(response.json(), {"ping": "successful", "ping_db": "successful: mock_db"})       # noqa: 501
        mock_session.assert_called_once()

        app.dependency_overrides.clear()
