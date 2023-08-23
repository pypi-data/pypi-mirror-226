"""
Given an applicants details and a jobs data, have LLM give a summary of their fit
"""
import json

from getajob.abstractions.models import UserAndDatabaseConnection, Entity
from getajob.vendor.openai.repository import OpenAIRepository
from getajob.contexts.users.details.repository import UserDetailsRepository
from getajob.contexts.companies.jobs.repository import JobsRepository

from .models import ApplicantFit


class ApplicationFitRepository:
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        self.user_details_repo = UserDetailsRepository(
            request_scope=request_scope, kafka=None
        )
        self.job_repo = JobsRepository(
            request_scope=request_scope, kafka=None, algolia_jobs=None
        )

    def get_job_fit_summary(self, user_id: str, company_id: str, job_id: str):
        user_details = self.user_details_repo.get_sub_entity(
            parent_collections={Entity.USERS.value: user_id},
        )
        job = self.job_repo.get(
            job_id, parent_collections={Entity.COMPANIES.value: company_id}
        )
        prompt = f"""Given the following user and job data,
        rate this applicant out of 10 tell me if this person is a good fit for this job
        User: {user_details.qualifications}
        Job: {job}
        """
        resp = OpenAIRepository().text_prompt(prompt=prompt, max_tokens=500)
        return ApplicantFit(**json.loads(resp))
