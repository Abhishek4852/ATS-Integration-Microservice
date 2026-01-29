from .base_provider import BaseATSProvider
import uuid

class WorkableProvider(BaseATSProvider):
    """Workable ATS Integration (Mock Implementation)"""

    def get_jobs(self):
        # Mock data for Workable
        raw_jobs = [
            {
                "shortcode": "wk-1",
                "title": "Backend Developer",
                "location": {"city": "Berlin"},
                "state": "published",
                "url": "https://workable.com/job/1"
            }
        ]
        return [self.normalize_job(j) for j in raw_jobs]

    def create_candidate(self, candidate_data):
        print(f"Workable: Creating candidate {candidate_data['name']}")
        return f"wk_can_{uuid.uuid4().hex[:8]}"

    def attach_candidate_to_job(self, candidate_id, job_id):
        print(f"Workable: Creating application for {candidate_id}")
        return f"wk_app_{uuid.uuid4().hex[:8]}"

    def get_applications(self, job_id):
        raw_apps = [
            {
                "id": "wk-app-1",
                "name": "Jane Smith",
                "email": "jane@example.com",
                "stage": "applied"
            }
        ]
        return [self.normalize_application(a) for a in raw_apps]

    def normalize_job(self, raw_job):
        return {
            "id": raw_job["shortcode"],
            "title": raw_job["title"],
            "location": raw_job["location"]["city"],
            "status": "OPEN" if raw_job["state"] == "published" else "CLOSED",
            "external_url": raw_job["url"]
        }

    def normalize_application(self, raw_app):
        status_map = {
            "applied": "APPLIED",
            "phone_screen": "SCREENING",
            "hired": "HIRED",
            "disqualified": "REJECTED"
        }
        return {
            "id": str(raw_app["id"]),
            "candidate_name": raw_app["name"],
            "email": raw_app["email"],
            "status": status_map.get(raw_app["stage"], "APPLIED")
        }
