from pydantic import BaseModel


class DefaultGroupDataClass(BaseModel):
    technical_name: str
    label: str


class UserGroupsDataClass(BaseModel):
    main_group: DefaultGroupDataClass
    groups: list[DefaultGroupDataClass]
