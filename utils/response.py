import json

def success_response(data, status_code=200):
    """Return a standard success response for API Gateway."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"  # Permissive CORS for development
        },
        "body": json.dumps(data)
    }

def error_response(message, status_code=400):
    """Return a standard error response for API Gateway."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "error": True,
            "message": message,
            "status_code": status_code
        })
    }
