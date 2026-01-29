import unittest
from unittest.mock import patch, MagicMock
from providers.zoho import ZohoProvider
from utils.errors import ATSError

class TestZohoProvider(unittest.TestCase):

    @patch('providers.zoho.settings')
    def setUp(self, mock_settings):
        mock_settings.ZOHO_CLIENT_ID = "test_id"
        mock_settings.ZOHO_CLIENT_SECRET = "test_secret"
        mock_settings.ZOHO_REFRESH_TOKEN = "test_refresh"
        mock_settings.ZOHO_BASE_URL = "https://recruit.zoho.com/recruit/v2"
        mock_settings.ZOHO_TOKEN_URL = "https://accounts.zoho.com/oauth/v2/token"
        self.provider = ZohoProvider()

    @patch('requests.post')
    def test_get_access_token_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "mock_access_token"}
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        token = self.provider._get_access_token()
        self.assertEqual(token, "mock_access_token")
        mock_post.assert_called_once()

    @patch('requests.get')
    @patch('providers.zoho.ZohoProvider._get_access_token')
    def test_get_jobs_success(self, mock_token, mock_get):
        mock_token.return_value = "mock_access_token"
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "123",
                    "Posting_Title": "Software Engineer",
                    "City": "San Francisco",
                    "Status": "In-progress"
                }
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        jobs = self.provider.get_jobs()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['title'], "Software Engineer")
        self.assertEqual(jobs[0]['status'], "OPEN")

    @patch('requests.post')
    @patch('providers.zoho.ZohoProvider._get_access_token')
    def test_create_candidate_success(self, mock_token, mock_post):
        mock_token.return_value = "mock_access_token"
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {
                    "status": "success",
                    "details": {"id": "cand_123"}
                }
            ]
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        candidate_data = {"name": "John Doe", "email": "john@example.com"}
        candidate_id = self.provider.create_candidate(candidate_data)
        self.assertEqual(candidate_id, "cand_123")

if __name__ == '__main__':
    unittest.main()
