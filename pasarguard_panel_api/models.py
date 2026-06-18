""" File with Pydantic models for validation """

from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field

from .enums import Status

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
    expire: Optional[datetime]
    data_limit: Optional[int]
    data_limit_reset_strategy: Optional[str]
    note: Optional[str]
    on_hold_expire_duration: Optional[int]
    on_hold_timeout: Optional[int]
    group_ids: list[int]
    auto_delete_in_days: Optional[int]
    next_plan: Optional[dict]
    id: int
    username: str
    status: str
    hwid_limit: Optional[int]
    used_traffic: int
    lifetime_used_traffic: Optional[int]
    created_at: datetime
    edit_at: Optional[datetime]
    online_at: Optional[datetime]
    subscription_url: Optional[str]
    admin: dict[str, Union[str, int]]


class Users(BaseModel):
    users: list[User]
    total: int


class NewUser(BaseModel):
    username: str = Field(min_length=4)
    status: str = Status.ACTIVE
    data_limit: int = 0
    expire: Union[datetime, int] = 0
    note: str = ""
    group_ids: list[int]
    proxy_settings: dict[str, dict] = {}
    next_plan: Optional[dict] = {}


class GeneralSettings(BaseModel):
    default_flow: Optional[str] = None
    default_method: str


class Group(BaseModel):
    id: int
    name: str
    inbound_tags: Optional[list[str]]
    is_disabled: bool
    total_users: int


class Groups(BaseModel):
    groups: list[Group]
    total: int
