import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    url = os.getenv("ZOHO_TOKEN_URL")
    params = {
        "refresh_token": os.getenv("ZOHO_REFRESH_TOKEN"),
        "client_id": os.getenv("ZOHO_CLIENT_ID"),
        "client_secret": os.getenv("ZOHO_CLIENT_SECRET"),
        "grant_type": "refresh_token"
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()["access_token"]

def get_fields(module):
    token = get_access_token()
    base_url = os.getenv("ZOHO_BASE_URL")
    url = f"{base_url}/settings/fields?module={module}"
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        print("Fetching fields for Candidates...")
        candidates_fields = get_fields("Candidates")
        for field in candidates_fields.get("fields", []):
            if field.get("data_type") == "lookup" or "Job" in field.get("field_label") or "Opening" in field.get("field_label"):
                print(f"Label: {field.get('field_label')}, API Name: {field.get('api_name')}, Type: {field.get('data_type')}")
        
        print("\nFetching fields for JobOpenings...")
        jobs_fields = get_fields("JobOpenings")
        for field in jobs_fields.get("fields", []):
            if field.get("data_type") == "lookup":
                 print(f"Label: {field.get('field_label')}, API Name: {field.get('api_name')}, Type: {field.get('data_type')}")
    except Exception as e:
        print(f"Error: {e}")
