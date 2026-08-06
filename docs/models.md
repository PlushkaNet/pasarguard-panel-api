# 🧱 Models reference

All models are Pydantic v2 `BaseModel` subclasses and are exported from the
package root:

```python
from pasarguard_panel_api import (
    SystemInfo, User, Users, NewUser, GeneralSettings,
    Group, Groups, Template, AdminMinimalInfo,
)
```

Every returned model supports the standard Pydantic helpers:
`.model_dump()`, `.model_dump_json()`, `.model_copy()`, `.model_fields`, etc.

## Enums

### `Status` (StrEnum)

User subscription statuses, usable directly in `User.status` /
`NewUser.status`:

| Member | Value |
| --- | --- |
| `Status.ACTIVE` | `"active"` |
| `Status.DISABLED` | `"disabled"` |
| `Status.LIMITED` | `"limited"` |
| `Status.EXPIRED` | `"expired"` |
| `Status.ON_HOLD` | `"on_hold"` |

Because it is a `StrEnum`, `Status` values can be compared with plain strings:

```python
assert Status.ACTIVE == "active"
```

---

## `SystemInfo`

Panel runtime statistics. Returned by `get_system_info()`.

| Field | Type | Description |
| --- | --- | --- |
| `version` | `str` | Panel version |
| `uptime_seconds` | `int` | Time since panel start |
| `mem_total` / `mem_used` | `int` | Memory usage (%/bytes) |
| `disk_total` / `disk_used` | `int` | Disk usage (%/bytes) |
| `cpu_cores` | `int` | CPU core count |
| `cpu_usage` | `float` | CPU usage percent |
| `total_user` | `int` | Total users |
| `online_users` | `int` | Currently online |
| `active_users` | `int` | Active subscriptions |
| `on_hold_users` | `int` | On-hold subscriptions |
| `disabled_users` | `int` | Disabled users |
| `expired_users` | `int` | Expired users |
| `limited_users` | `int` | Data-limited users |
| `incoming_bandwidth` | `int` | Total inbound bytes |
| `outgoing_bandwidth` | `int` | Total outbound bytes |

---

## `GeneralSettings`

General panel settings. Returned by `get_general_info()`.

| Field | Type | Description |
| --- | --- | --- |
| `default_flow` | `str \| None` | Default proxy flow |
| `default_method` | `str` | Default proxy method (e.g. for Shadowsocks) |

```python
info = pg.get_general_info()
proxy_settings = {"shadowsocks": {"method": info.default_method}}
```

---

## `Group` / `Groups`

Group info; `Groups` is the envelope returned by `get_groups()`.

> Note: only superuser can request groups

`Group`:

| Field | Type | Description |
| --- | --- | --- |
| `id` | `int` | Group ID (use in `group_ids`) |
| `name` | `str` | Group name |
| `inbound_tags` | `list[str] \| None` | Associated inbound tags |
| `is_disabled` | `bool \| None` | Whether the group is disabled |
| `total_users` | `int \| None` | Users in the group |

`Groups`:

| Field | Type | Description |
| --- | --- | --- |
| `groups` | `list[Group]` | Full list of groups |
| `total` | `int` | Number of groups |

---

## `User`

Full user object. Returned by `add_user()`, `get_user()`, `modify_user()`,
`from_template()`; embedded in `Users.users`.

| Field | Type | Description |
| --- | --- | --- |
| `id` | `int` | User ID |
| `username` | `str` | Username |
| `status` | `str` | Subscription status (see `Status`) |
| `proxy_settings` | `dict[str, dict]` | Per-protocol proxy settings |
| `expire` | `datetime \| None` | Subscription expiry |
| `data_limit` | `int \| None` | Data limit (bytes) |
| `data_limit_reset_strategy` | `str \| None` | Reset strategy |
| `note` | `str \| None` | Admin note |
| `on_hold_expire_duration` | `int \| None` | On-hold expire duration |
| `on_hold_timeout` | `int \| None` | On-hold timeout |
| `group_ids` | `list[int]` | Assigned groups |
| `auto_delete_in_days` | `int \| None` | Auto-delete countdown |
| `next_plan` | `dict \| None` | Upcoming plan |
| `hwid_limit` | `int \| None` | Hardware ID limit |
| `used_traffic` | `int` | Current-period traffic (bytes) |
| `lifetime_used_traffic` | `int \| None` | Lifetime traffic (bytes) |
| `created_at` | `datetime` | Creation time |
| `edit_at` | `datetime \| None` | Last edit time |
| `online_at` | `datetime \| None` | Last seen online |
| `subscription_url` | `str \| None` | Subscription URL path, e.g. `/sub/ia9Akdcn2usaJs` |
| `admin` | `AdminMinimalInfo` | Owner admin (`id`, `username`) |

> **Modification pattern:** fetch → mutate fields → `modify_user(user)`.
> Fields mutated on the model are sent verbatim, so make sure edits are
> intentional (e.g. extend `expire`, flip `status`, change `group_ids`).

---

## `Users`

Paginated search result. Returned by `get_users()`.

| Field | Type | Description |
| --- | --- | --- |
| `users` | `list[User]` | Users on this page |
| `total` | `int` | Total matching users (across all pages) |

```python
result = pg.get_users(limit=10)
print(len(result.users), "of", result.total)
```

---

## `NewUser`

Request model for `add_user()`. All fields have defaults except
`username` and `group_ids`.

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `username` | `str` | **required** | Username, **min 4 characters** (validated) |
| `status` | `str` | `Status.ACTIVE` | Initial status |
| `data_limit` | `int` | `0` | Data limit in bytes (`0` = unlimited) |
| `expire` | `datetime \| int` | `0` | Expiry (datetime or unix timestamp) |
| `note` | `str` | `""` | Admin note |
| `group_ids` | `list[int]` | **required** | Group IDs from `get_groups()` |
| `proxy_settings` | `dict[str, dict]` | `{}` | Per-protocol settings |
| `next_plan` | `dict \| None` | `{}` | Upcoming plan |

```python
from datetime import datetime, timedelta, timezone

NewUser(
    username="alice",
    group_ids=[1, 2],
    expire=datetime.now(timezone.utc) + timedelta(weeks=4),
    proxy_settings={
        "vless": {},
        "shadowsocks": {"method": info.default_method},
    },
)
```

---

## `Template`

Template info (used with `from_template()`; not returned by any current
method but parsed by the panel API).

| Field | Type |
| --- | --- |
| `name` | `str` |
| `data_limit` | `int` |
| `hwid_limit` | `int \| None` |
| `expire_duration` | `int \| None` |
| `username_prefix` / `username_suffix` | `str` |
| `group_ids` | `list[int]` |
| `extra_settings` | `dict` |
| `status` | `str` |
| `reset_usages` | `bool` |
| `on_hold_timeout` | `int \| None` |
| `data_limit_reset_strategy` | `str` |
| `is_disabled` | `bool` |
| `id` | `int` |

---

## `AdminMinimalInfo`

Minimal info about the admin that owns a user.

| Field | Type |
| --- | --- |
| `id` | `int` |
| `username` | `str` |
