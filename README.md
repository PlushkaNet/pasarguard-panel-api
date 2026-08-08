[![python-versions-supported](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/)
[![pypi-version](https://img.shields.io/pypi/v/pasarguard-panel-api)](https://pypi.org/project/pasarguard-panel-api/)
[![pypi-downloads](https://img.shields.io/pypi/dm/pasarguard-panel-api)](https://pypistats.org/packages/pasarguard-panel-api)
[![panel-version-supported](https://img.shields.io/badge/panel-V5-black)](https://github.com/PasarGuard/panel)
[![license](https://img.shields.io/badge/license-MIT-green)](https://raw.githubusercontent.com/PlushkaNet/pasarguard-panel-api/refs/heads/main/LICENSE)

# 🛠️ pasarguard-panel-api

> Sync & async Python SDK for interacting with the [Pasarguard](https://github.com/PasarGuard/panel) panel API.

A minimal, type-safe wrapper around the Pasarguard user-management API.
Built on [httpx](https://www.python-httpx.org/) for networking and
[pydantic v2](https://pydantic.dev/docs/) for response validation.

## 🔥 Features

- **Sync & async clients** with an identical interface — write the code once, run it in both worlds
- **Automatic token handling** — the client logs in for you and transparently renews the token when it expires (401 → re-auth → retry)
- **Type-safe responses** — every method returns validated Pydantic models
- **Minimal & lean** — a small, readable codebase, no hidden magic
- **Typing support** — ships with `py.typed`, fully annotated public API

## 📦 Installation

Requires Python **3.11+**.

```bash
pip install pasarguard-panel-api
```

## 🚀 Quick start

### Sync

```python
from os import getenv
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv # requires `dotenv` package
from pasarguard_panel_api import Pasarguard, NewUser, Status

load_dotenv() # load environment variables

pg = Pasarguard(getenv("host"), getenv("user"), getenv("password"))
pg.auth() # request an auth token

# get available groups (`get_groups` requires admin privilegies)
groups = pg.get_groups()

# create a new user
user = pg.add_user(
    NewUser(
        username="new-user",
        status=Status.ACTIVE,
        expire=datetime.now(tz=timezone.utc) + timedelta(weeks=1), # 1 week subscription
        group_ids=[groups.groups[0].id], # or id that you know, e.g: 4
    )
)

print(user.subscription_url)
```

### Async

```python
import asyncio
from os import getenv
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv # requires `dotenv` package
from pasarguard_panel_api import AsyncPasarguard, NewUser, Status

load_dotenv() # load environment variables

pg = AsyncPasarguard(getenv("host"), getenv("user"), getenv("password"))

async def main():
    await pg.auth()
    # `get_groups` requires admin privilegies
    groups = await pg.get_groups()
    user = await pg.add_user(
        NewUser(
            username="new-user",
            status=Status.ACTIVE,
            expire=datetime.now(tz=timezone.utc) + timedelta(weeks=1), # 1 week subscription
            group_ids=[groups.groups[0].id], # or id that you know, e.g: 4
        )
    )
    print(user.subscription_url)

asyncio.run(main())
```

> **Note:** The API interface is identical for both sync and async operations — only `await` is added.
> Authentication is optional: if you skip `auth()`, the client will log in automatically on the first request.

## 📚 API overview

| Method | Description | Returns |
| --- | --- | --- |
| `auth()` | Obtain an auth token from the panel | `None` |
| `get_system_info()` | Panel version, uptime, memory/CPU usage, user stats | `SystemInfo` |
| `get_general_info()` | General settings, e.g. default proxy method | `GeneralSettings` |
| `get_groups()` | List of user groups | `Groups` |
| `get_users(**filters)` | Search users with filters | `Users` |
| `get_user(pattern)` | Find a single user by name pattern | `User \| None` |
| `add_user(NewUser)` | Create a new user | `User` |
| `modify_user(User)` | Update an existing user | `User` |
| `from_template(name, template_id)` | Create a user from a template | `User \| None` |

### Search filters for `get_users`

| Argument | Type | Default |
| --- | --- | --- |
| `limit` | `int` | `10` |
| `sort` | `str` | `"-created_at"` |
| `load_sub` | `bool` | `True` |
| `offset` | `int` | `0` |
| `is_protocol` | `bool` | `False` |
| `search` | `str` | — |

## ✏️ Examples

```python
# Search & modify users (sync)
user = pg.get_user("some-username")
assert user is not None # ensure that this user exists

user.status = Status.DISABLED # disable the user
user.expire = user.expire + timedelta(weeks=1) # extend subscription
modified = pg.modify_user(user)

# Create a user from a template
user = pg.from_template("new-user", 3) # 3 - template number

# System health
stats = pg.get_system_info()
print(stats.online_users)
```

> The async versions of all the above are identical, just add `await`.

📄 More complete examples live in the [`examples/`](https://github.com/PlushkaNet/pasarguard-panel-api/tree/main/examples) directory.

## 📖 Documentation

Full documentation is available in the [`docs/`](https://github.com/PlushkaNet/pasarguard-panel-api/tree/main/docs) directory:

- [Quick start](https://github.com/PlushkaNet/pasarguard-panel-api/tree/main/docs/quickstart.md)
- [API reference](https://github.com/PlushkaNet/pasarguard-panel-api/tree/main/docs/api-reference.md)
- [Models reference](https://github.com/PlushkaNet/pasarguard-panel-api/tree/main/docs/models.md)
- [Authentication](https://github.com/PlushkaNet/pasarguard-panel-api/tree/main/docs/authentication.md)
- [Error handling](https://github.com/PlushkaNet/pasarguard-panel-api/tree/main/docs/errors.md)

## ℹ️ About

**What this SDK does:** it gives you a fast, simple way to interact with
Pasarguard's user management endpoints, without the bloat of a full-featured
implementation. The code is kept lean and readable. This is a **minimal**
wrapper — not a complete API coverage.

**Limitations:** the client opens a fresh HTTP connection per request and
currently covers the user-management surface of the API (users, groups,
templates, system info, settings). Endpoints outside that scope are not
implemented yet — PRs welcome.

## ✏️ Contributing

Bug reports, feature requests and pull requests are welcome — feel free to
open issues and PRs.

**❤️ Special thanks to the Pasarguard team for the wonderful panel that makes proxy management easier!**

## 📄 License

[MIT](https://github.com/PlushkaNet/pasarguard-panel-api/tree/main/LICENSE)
