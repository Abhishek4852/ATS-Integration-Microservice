import requests
import json
from .base_provider import BaseATSProvider
from config.settings import settings
from utils.errors import ATSError
from utils.pagination import paginate_all

class ZohoProvider(BaseATSProvider):
    """Zoho Recruit ATS Integration"""

    def __init__(self):
        self.client_id = settings.ZOHO_CLIENT_ID
        self.client_secret = settings.ZOHO_CLIENT_SECRET
        self.refresh_token = settings.ZOHO_REFRESH_TOKEN
        self.base_url = settings.ZOHO_BASE_URL
        self.token_url = settings.ZOHO_TOKEN_URL
        self._access_token = None

    def _get_access_token(self):
        """Fetch access token using refresh token."""
        if self._access_token:
            return self._access_token

        payload = {
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token"
        }
        
        try:
            response = requests.post(self.token_url, params=payload)
            response.raise_for_status()
            data = response.json()
            if "access_token" not in data:
                raise ATSError(f"Failed to get access token: {data.get('error', 'Unknown error')}", 401)
            
            self._access_token = data["access_token"]
            return self._access_token
        except requests.exceptions.RequestException as e:
            raise ATSError(f"Zoho Auth Error: {str(e)}", 401)

    def _get_headers(self):
        return {
            "Authorization": f"Zoho-oauthtoken {self._get_access_token()}",
            "Content-Type": "application/json"
        }

    def get_jobs(self):
        """Fetch all job openings from Zoho Recruit using pagination."""
        return paginate_all(self._fetch_jobs_page)

    def _fetch_jobs_page(self, page=1):
        """Fetch a single page of job openings."""
        # Zoho Recruit uses 'page' and 'per_page' (or 'fromIndex' in older APIs)
        # For the current API, let's use page and default per_page (usually 200)
        url = f"{self.base_url}/JobOpenings"
        params = {"page": page}
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            
            if response.status_code == 204 or not response.text:
                return []
                
            response.raise_for_status()
            data = response.json()
            raw_jobs = data.get("data", [])
            return [self.normalize_job(j) for j in raw_jobs]
        except requests.exceptions.RequestException as e:
            raise ATSError(f"Zoho API Error: {str(e)}", 500)
        except json.JSONDecodeError:
            raise ATSError("Zoho API Error: Received invalid JSON response", 500)

    def create_candidate(self, candidate_data):
        """Create a candidate in Zoho Recruit, or return existing ID if duplicate."""
        url = f"{self.base_url}/Candidates"
        
        email = candidate_data.get("email")
        name_parts = candidate_data.get("name", "").split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else "N/A"

        payload = {
            "data": [
                {
                    "First_Name": first_name,
                    "Last_Name": last_name,
                    "Email": email,
                    "Mobile": candidate_data.get("phone", "")
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=self._get_headers(), data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            
            data = result.get("data", [{}])[0]
            
            # Handle success
            if data.get("status") == "success":
                return data.get("details", {}).get("id")
            
            # Handle duplicate error
            if data.get("status") == "error" and (data.get("code") == "DUPLICATE_DATA" or "Duplicate values" in data.get("message", "")):
                print(f"Zoho Debug: Candidate {email} already exists. Searching for existing ID...")
                return self._search_candidate_by_email(email)
                
            if data.get("status") == "error":
                raise ATSError(f"Zoho Candidate Creation Error: {data.get('message')}", 400)
            
            return data.get("details", {}).get("id")
        except requests.exceptions.RequestException as e:
            raise ATSError(f"Zoho API Error: {str(e)}", 500)

    def _search_candidate_by_email(self, email):
        """Search for a candidate ID by email address."""
        url = f"{self.base_url}/Candidates/search"
        params = {"criteria": f"Email:equals:{email}"}
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            data = response.json()
            
            candidates = data.get("data", [])
            if candidates:
                existing_id = candidates[0].get("id")
                print(f"Zoho Debug: Found existing candidate ID: {existing_id}")
                return existing_id
                
            raise ATSError(f"Could not find existing candidate with email {email} despite duplicate error.", 404)
        except requests.exceptions.RequestException as e:
            raise ATSError(f"Zoho Search Error: {str(e)}", 500)

    def attach_candidate_to_job(self, candidate_id, job_id):
        """Associate a candidate with a job opening."""
        url = f"{self.base_url}/Candidates/actions/associate"
        
        payload = {
          "data": [
            {
              "ids": [candidate_id],
              "jobids": [job_id],
              "status": "Associated"
            }
          ]
        }
        
        try:
            response = requests.put(url, headers=self._get_headers(), data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            
            data = result.get("data", [{}])[0]
            if data.get("status") == "error":
                raise ATSError(f"Zoho Association Error: {data.get('message')}", 400)
            
            return f"{candidate_id}_{job_id}"
        except requests.exceptions.RequestException as e:
            error_body = ""
            if hasattr(e, 'response') and e.response is not None:
                error_body = e.response.text
            print(f"Zoho Debug: Association failed. URL: {url} - Body: {error_body}")
            raise ATSError(f"Zoho API Error: {str(e)}", 500)

    def get_applications(self, job_id):
        """Fetch all applications for a job using pagination."""
        return paginate_all(self._fetch_applications_page, job_id=job_id)

    def _fetch_applications_page(self, page=1, job_id=None):
        """Fetch a single page of applications for a job."""
        url = f"{self.base_url}/Applications/search"
        params = {
            "criteria": f"($Job_Opening_Id:equals:{job_id})",
            "page": page
        }
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            
            if response.status_code == 204:
                return []
                
            response.raise_for_status()
            data = response.json()
            raw_apps = data.get("data", [])
            
            return [self.normalize_application(a) for a in raw_apps]
        except requests.exceptions.RequestException as e:
            print(f"Warning: Failed to fetch applications for job {job_id} page {page}: {str(e)}")
            return []

    def normalize_job(self, raw_job):
        return {
            "id": str(raw_job.get("id")),
            "title": raw_job.get("Posting_Title"),
            "location": raw_job.get("City", "N/A"),
            "status": "OPEN" if raw_job.get("Status") == "In-progress" else "CLOSED",
            "external_url": f"https://recruit.zoho.com/recruit/ViewJob.na?digest={raw_job.get('id')}"
        }

    def normalize_application(self, raw_app):
        # The Applications module has candidate info directly or in fields like Full_Name, Email
        candidate_name = raw_app.get("Full_Name") or "Unknown"
        # If Full_Name is missing, try First/Last
        if candidate_name == "Unknown":
            first = raw_app.get("First_Name", "")
            last = raw_app.get("Last_Name", "")
            candidate_name = f"{first} {last}".strip() or "Unknown"

        return {
            "id": str(raw_app.get("id")),
            "candidate_name": candidate_name,
            "email": raw_app.get("Email", "N/A"),
            "status": raw_app.get("Application_Status", "APPLIED")
        }
