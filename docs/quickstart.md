# 🚀 Quick start

## Requirements

- Python **3.11+**
- A running Pasarguard panel with an admin account (`host` URL, `user`, `password`)

## Installation

```bash
pip install pasarguard-panel-api
```

To install from source:

```bash
git clone https://github.com/PlushkaNet/pasarguard-panel-api.git
cd pasarguard-panel-api
pip install .
```

## Choosing sync or async

The package exposes two equivalent clients:

| Client | Use when |
| ---  | --- |
| `Pasarguard` | scripts, CLI tools, sync frameworks |
| `AsyncPasarguard` | asyncio apps, FastAPI, bots, high concurrency |

Both classes share the **exact same method names, signatures and return types**.
The only difference is that async methods must be awaited. Code written against
one client can be switched to the other by changing the class name and adding
(or removing) `await`.

## First steps

### 1. Initialize the client

```python
from pasarguard_panel_api import Pasarguard

pg = Pasarguard("https://panel.example.com", "admin", "secret")
```

Notes:

- A trailing slash on the URL is stripped automatically.
- **No request is made yet** — the client only stores credentials.

### 2. Authenticate (optional)

```python
pg.auth()
```

`auth()` requests an access token from `POST /api/admin/token`.
If you skip this call, the client logs in **automatically** on the first API
request, so `auth()` is only needed if you want to fail fast with a clear
`AuthorizationError` when credentials are wrong.

### 3. Make requests

```python
info = pg.get_system_info()          # panel health
groups = pg.get_groups()             # user groups
users = pg.get_users(limit=50)       # search users
```

Every method returns a validated Pydantic model (see [models](models.md)).

### 4. Run asynchronously

```python
import asyncio
from pasarguard_panel_api import AsyncPasarguard

async def main():
    pg = AsyncPasarguard("https://panel.example.com", "admin", "secret")
    await pg.auth()
    users = await pg.get_users(limit=50)
    print(users.total)

asyncio.run(main())
```

## Minimal end-to-end example

Create a user, hand out the subscription URL, extend it a week later:

```python
from datetime import datetime, timedelta, timezone
from pasarguard_panel_api import Pasarguard, NewUser, Status

pg = Pasarguard("https://panel.example.com", "admin", "secret")

groups = pg.get_groups()

user = pg.add_user(
    NewUser(
        username="alice",
        status=Status.ACTIVE,
        group_ids=[groups.groups[0].id],
        expire=datetime.now(timezone.utc) + timedelta(weeks=4),
        data_limit=0, # unlimited
    )
)

print(user.subscription_url) # give this to the user
```

## Environment variables

The examples load credentials from a `.env` file via `python-dotenv`:

```
host=https://panel.example.com
user=admin
password=secret
```

`python-dotenv` is **not** a dependency of the package itself — install it
separately (`pip install python-dotenv`) or hardcode/config your credentials
any way you like.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `AuthorizationError` | Wrong `host` / `user` / `password` |
| `APIResponseError` | Request rejected by the panel (see the message body) |
| `UserAlreadyExistsError` | Username is already taken |
| Pydantic `ValidationError` | Panel returned data the models don't understand (e.g. panel version mismatch) |

See [errors](errors.md) for the full picture.
