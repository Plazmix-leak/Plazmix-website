from pydantic import BaseModel


class BuilderFormDataClass(BaseModel):
    first_name: str
    last_name: str
    years: int
    vk: str
    timezone: str
    project_time: str
    experiences: str
    motivation: str
    jobs: str
    about_us: str
