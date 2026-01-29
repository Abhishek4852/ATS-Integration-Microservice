import json
from services.jobs_service import JobsService
from services.candidate_service import CandidateService
from services.application_service import ApplicationService
from utils.response import success_response, error_response
from utils.errors import ATSError

def get_jobs(event, context):
    """GET /jobs"""
    try:
        service = JobsService()
        jobs = service.list_jobs()
        return success_response(jobs)
    except ATSError as e:
        return error_response(e.message, e.status_code)
    except Exception as e:
        print(f"Unhandled error: {str(e)}")
        return error_response("Internal Server Error", 500)

def create_candidate(event, context):
    """POST /candidates"""
    try:
        body = json.loads(event.get("body") or "{}")
        service = CandidateService()
        application_id = service.apply_to_job(body)
        
        return success_response({
            "message": "Candidate applied successfully",
            "application_id": application_id
        }, status_code=201)
    except ATSError as e:
        return error_response(e.message, e.status_code)
    except Exception as e:
        print(f"Unhandled error: {str(e)}")
        return error_response("Internal Server Error", 500)

def get_applications(event, context):
    """GET /applications?job_id=JOB_ID"""
    try:
        query_params = event.get("queryStringParameters") or {}
        job_id = query_params.get("job_id")
        
        service = ApplicationService()
        applications = service.list_applications(job_id)
        
        return success_response(applications)
    except ATSError as e:
        return error_response(e.message, e.status_code)
    except Exception as e:
        print(f"Unhandled error: {str(e)}")
        return error_response("Internal Server Error", 500)
