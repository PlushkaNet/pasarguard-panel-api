"""
File with Pydantic models for validation data from Pasarguard panel V5
"""

from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field

from .enums import Status

class SystemInfo(BaseModel):
    """Pasarguard system info model"""
    version: str
    uptime_seconds: int
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

class AdminMinimalInfo(BaseModel):
    """Model with information about user's administrator"""
    id: int
    username: str

class User(BaseModel):
    """Model with information about user"""
    proxy_settings: dict[str, dict]
    expire: Optional[datetime] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: Optional[str] = None
    note: Optional[str] = None
    on_hold_expire_duration: Optional[int] = None
    on_hold_timeout: Optional[int] = None
    group_ids: list[int]
    auto_delete_in_days: Optional[int] = None
    next_plan: Optional[dict] = {}
    id: int
    username: str
    status: str
    hwid_limit: Optional[int] = None
    used_traffic: int
    lifetime_used_traffic: Optional[int] = None
    created_at: datetime
    edit_at: Optional[datetime] = None
    online_at: Optional[datetime] = None
    subscription_url: Optional[str] = None
    admin: AdminMinimalInfo

class Users(BaseModel):
    """Model with information about users from `get_users` method"""
    users: list[User]
    total: int

class NewUser(BaseModel):
    """Model with information about new user that will be created"""
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
    """Model with information about group of users"""
    id: int
    name: str
    inbound_tags: Optional[list[str]] = []
    is_disabled: Optional[bool] = None
    total_users: Optional[int] = None

class Groups(BaseModel):
    """Model with information about groups"""
    groups: list[Group]
    total: int

class Template(BaseModel):
    """Model with information about user template"""
    name: str
    data_limit: int
    hwid_limit: Optional[int] = None
    expire_duration: Optional[int] = None
    username_prefix: str
    username_suffix: str
    group_ids: list[int]
    extra_settings: dict
    status: str
    reset_usages: bool
    on_hold_timeout: Optional[int] = None
    data_limit_reset_strategy: str
    is_disabled: bool
    id: int
