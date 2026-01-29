from abc import ABC, abstractmethod

class BaseATSProvider(ABC):
    """
    Abstract base class for ATS providers.
    All ATS specific logic must be encapsulated in subclasses.
    """

    @abstractmethod
    def get_jobs(self):
        """
        Fetch all jobs from the ATS and normalize them.
        :return: List of normalized job dictionaries.
        """
        pass

    @abstractmethod
    def create_candidate(self, candidate_data):
        """
        Create a candidate in the ATS.
        :param candidate_data: Dict containing name, email, phone, etc.
        :return: Internal candidate ID.
        """
        pass

    @abstractmethod
    def attach_candidate_to_job(self, candidate_id, job_id):
        """
        Link a candidate to a specific job opening.
        :return: Application/Pipeline entry ID.
        """
        pass

    @abstractmethod
    def get_applications(self, job_id):
        """
        Fetch applications for a specific job and normalize them.
        :return: List of normalized application dictionaries.
        """
        pass

    def normalize_job(self, raw_job):
        """Standardize job fields across different ATS."""
        raise NotImplementedError

    def normalize_application(self, raw_app):
        """Standardize application fields across different ATS."""
        raise NotImplementedError
