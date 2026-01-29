from .base_provider import BaseATSProvider
from utils.pagination import paginate_all
import uuid

class GreenhouseProvider(BaseATSProvider):
    """Greenhouse ATS Integration (Mock Implementation)"""

    def get_jobs(self):
        # Fetching all pages internally
        return paginate_all(self._fetch_jobs_page)

    def _fetch_jobs_page(self, page):
        # Mock data for Greenhouse
        if page > 1: return [] # Only return 1 page for mock
        
        raw_jobs = [
            {
                "id": "gh-1",
                "title": "Software Engineer",
                "location": {"name": "Remote"},
                "status": "active",
                "absolute_url": "https://boards.greenhouse.io/job/1"
            },
            {
                "id": "gh-2",
                "title": "Product Manager",
                "location": {"name": "New York"},
                "status": "active",
                "absolute_url": "https://boards.greenhouse.io/job/2"
            }
        ]
        return [self.normalize_job(j) for j in raw_jobs]

    def create_candidate(self, candidate_data):
        # Mock candidate creation
        print(f"Greenhouse: Creating candidate {candidate_data['email']}")
        return f"can_{uuid.uuid4().hex[:8]}"

    def attach_candidate_to_job(self, candidate_id, job_id):
        # Mock application creation
        print(f"Greenhouse: Attaching candidate {candidate_id} to job {job_id}")
        return f"app_{uuid.uuid4().hex[:8]}"

    def get_applications(self, job_id):
        # Mock fetching applications for a job
        raw_apps = [
            {
                "id": "gh-app-1",
                "candidate": {"first_name": "John", "last_name": "Doe", "email": "john@example.com"},
                "status": "initial_review"
            }
        ]
        return [self.normalize_application(a) for a in raw_apps]

    def normalize_job(self, raw_job):
        return {
            "id": str(raw_job["id"]),
            "title": raw_job["title"],
            "location": raw_job["location"]["name"],
            "status": "OPEN" if raw_job["status"] == "active" else "CLOSED",
            "external_url": raw_job["absolute_url"]
        }

    def normalize_application(self, raw_app):
        # Map statuses: initial_review -> SCREENING, etc.
        status_map = {
            "initial_review": "SCREENING",
            "active": "APPLIED",
            "hired": "HIRED",
            "rejected": "REJECTED"
        }
        return {
            "id": str(raw_app["id"]),
            "candidate_name": f"{raw_app['candidate']['first_name']} {raw_app['candidate']['last_name']}",
            "email": raw_app["candidate"]["email"],
            "status": status_map.get(raw_app["status"], "APPLIED")
        }
