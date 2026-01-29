from .jobs_service import get_provider
from utils.errors import ValidationError

class ApplicationService:
    def __init__(self):
        self.provider = get_provider()

    def list_applications(self, job_id):
        """Fetch normalized applications for a job."""
        if not job_id:
            raise ValidationError("job_id query parameter is required.")
            
        return self.provider.get_applications(job_id)
