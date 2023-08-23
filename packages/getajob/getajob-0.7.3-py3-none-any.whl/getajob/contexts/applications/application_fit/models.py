from pydantic import BaseModel


class ApplicantFit(BaseModel):
    score_out_of_ten: int
    summary: str
