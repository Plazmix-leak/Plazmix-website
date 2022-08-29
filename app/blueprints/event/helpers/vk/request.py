from pydantic import BaseModel


class VkWallRequest(BaseModel):
    id: int = None
    owner_id: int = None
    from_id: int = None
    created_by: int = None
    date: int = None
    text: str = None
    reply_owner_id: int = None
    post_type: str = None
    signer_id: int = None
    can_pin: int = None
    can_delete: int = None
    can_edit: int = None
    is_pinned: int = None
    marked_as_ads: int = None
    is_favorite: bool = None
    postponed_id: int = None
    attachments: list = None
