from pydantic import BaseModel


class ModeratorFormDataClass(BaseModel):
    first_name: str
    last_name: str
    years: int
    vk: str
    timezone: str
    project_time: str
    experiences: str
    motivation: str
    about_us: str
    microphone: str
    interview: str
