from config.settings import settings
from providers.greenhouse import GreenhouseProvider
from providers.workable import WorkableProvider
from utils.errors import ProviderNotFoundError

def get_provider():
    """Factory to get the active ATS provider."""
    provider_name = settings.ATS_PROVIDER
    if provider_name == "greenhouse":
        return GreenhouseProvider()
    elif provider_name == "workable":
        return WorkableProvider()
    elif provider_name == "zoho":
        from providers.zoho import ZohoProvider
        return ZohoProvider()
    else:
        raise ProviderNotFoundError(provider_name)

class JobsService:
    def __init__(self):
        self.provider = get_provider()

    def list_jobs(self):
        """Fetch and return normalized jobs from the active ATS."""
        return self.provider.get_jobs()
