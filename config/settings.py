import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Settings:
    """Centralized configuration for the ATS Integration Microservice."""
    
    ATS_PROVIDER = os.getenv("ATS_PROVIDER", "greenhouse").lower()
    ATS_API_KEY = os.getenv("ATS_API_KEY", "")
    ATS_BASE_URL = os.getenv("ATS_BASE_URL", "https://api.mockats.com")
    ATS_ACCOUNT_ID = os.getenv("ATS_ACCOUNT_ID", "")

    # Zoho Specific
    ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID", "")
    ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET", "")
    ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN", "")
    ZOHO_BASE_URL = os.getenv("ZOHO_BASE_URL", "https://recruit.zoho.com/recruit/v2")
    ZOHO_TOKEN_URL = os.getenv("ZOHO_TOKEN_URL", "https://accounts.zoho.com/oauth/v2/token")

    # Define supported providers
    SUPPORTED_PROVIDERS = ["greenhouse", "workable", "zoho"]

    @classmethod
    def validate(cls):
        """Simple validation for required settings."""
        if not cls.ATS_API_KEY:
            # We don't raise error here to allow mock/dev environment if needed
            # but in production, this would be critical
            print("Warning: ATS_API_KEY is not set.")
        
        if cls.ATS_PROVIDER not in cls.SUPPORTED_PROVIDERS:
            print(f"Warning: Unsupported ATS provider: {cls.ATS_PROVIDER}")

# Initialize settings
settings = Settings()
settings.validate()
