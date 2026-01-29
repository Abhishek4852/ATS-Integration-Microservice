from .jobs_service import get_provider
from utils.errors import ValidationError

class CandidateService:
    def __init__(self):
        self.provider = get_provider()

    def apply_to_job(self, data):
        """
        Orchestrate candidate creation and job attachment.
        1. Create candidate
        2. Attach to job
        """
        required_fields = ["name", "email", "job_id"]
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")

        # 1. Create candidate in ATS
        candidate_id = self.provider.create_candidate(data)
        
        # 2. Attach candidate to job (creates application)
        application_id = self.provider.attach_candidate_to_job(candidate_id, data["job_id"])
        
        return application_id
