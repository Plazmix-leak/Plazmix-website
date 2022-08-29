from pydantic import BaseModel


class YouTubeFormDataClass(BaseModel):
    channel_link: str
    average_views: str
    screen_shot: str
    video_release: str
