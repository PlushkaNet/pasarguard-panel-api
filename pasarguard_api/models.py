from pydantic import BaseModel, Field
from datetime import datetime

class SystemInfo(BaseModel):
    version: str
    mem_total: int
    mem_used: int
    disk_total: int
    disk_used: int
    cpu_cores: int
    cpu_usage: float
    total_user: int
    online_users: int
    active_users: int
    on_hold_users: int
    disabled_users: int
    expired_users: int
    limited_users: int
    incoming_bandwidth: int
    outgoing_bandwidth: int


class User(BaseModel):
    proxy_settings: dict[str, dict]
    expire: datetime | None = None
    data_limit: int | None = None
    data_limit_reset_strategy: str
    note: str | None = None
    on_hold_expire_duration: int | None = None
    on_hold_timeout: int | None = None
    group_ids: list[int]
    auto_delete_in_days: int | None = None
    next_plan: str | None = None #!
    id: int
    username: str
    status: str
    used_traffic: int
    lifetime_used_traffic: int
    created_at: datetime
    edit_at: datetime | None = None
    online_at: datetime | None = None
    subscription_url: str | None = None
    admin: dict[str, str]


class Users(BaseModel):
    users: list[User]
    total: int


class NewUser(BaseModel):
    username:str = Field(min_length=4)
    status:str = "active"
    data_limit:int = 0
    expire: int | datetime = 0
    note:str = ""
    group_ids:list[int]
    proxy_settings:dict[str, dict]
    next_plan:str | None = None


class GeneralSettings(BaseModel):
    default_flow:str | None = None
    default_method:str


class Group(BaseModel):
    id:int
    name:str


class Groups(BaseModel):
    groups:list[Group]
    total:int