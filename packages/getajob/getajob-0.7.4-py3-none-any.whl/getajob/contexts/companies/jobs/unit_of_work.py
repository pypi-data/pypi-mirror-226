from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity

from .models import CreateJob, UserCreateJob, Job


class JobsUnitOfWork:
    def __init__(self, job_repo: BaseRepository):
        self.repo = job_repo

    def create_job(self, company_id: str, data: UserCreateJob) -> Job:
        new_job = CreateJob(**data.dict(), is_live=False)
        return self.repo.create(
            new_job, parent_collections={Entity.COMPANIES.value: company_id}
        )

    def post_job(self, company_id: str, job_id: str):
        return self.repo.update(
            job_id,
            data={"is_live": True, "draft": False},
            parent_collections={Entity.COMPANIES.value: company_id},
        )
