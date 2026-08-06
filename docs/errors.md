# ⚠️ Error handling

## Exception hierarchy

All SDK-specific exceptions inherit from a common base, so you can catch
broad or narrow as needed:

```
PasarguardError (base)
├── AuthorizationError       — failed authentication (wrong credentials)
├── UserAlreadyExistsError   — HTTP 409 when creating a user that exists
└── APIResponseError         — any other non-200/201 response from the API
```

```python
from pasarguard_panel_api import PasarguardError, AuthorizationError
```

## What each exception means

### `AuthorizationError`

Raised when `POST /api/admin/token` does not return `200` — usually wrong
username/password or host.

```python
try:
    pg.auth()
except AuthorizationError as e:
    print("auth failed:", e)
```

### `UserAlreadyExistsError`

Raised by `add_user()` and `from_template()` when the panel answers
`HTTP 409 (Conflict)` — a user with that username already exists.

```python
try:
    pg.add_user(NewUser(username="alice", group_ids=[1]))
except UserAlreadyExistsError:
    print("username taken")
```

### `APIResponseError`

Raised for any API response outside `200`/`201` (other than the cases
mapped above). The message contains the status code and the response body,
which usually explains the panel-side reason.

```python
except APIResponseError as e:
    print(e) # e.g. "Unprocessable status: 422 with message: {...}"
```

### Third-party exceptions that can leak through

The SDK deliberately does not wrap errors from its dependencies — you may
see these directly:

- `httpx` transport errors — `httpx.ConnectError`, `httpx.TimeoutException`,
  `httpx.NetworkError`, etc. (panel unreachable, DNS, TLS, timeouts).
- `pydantic.ValidationError` — the panel returned data the models cannot
  parse. Usually means a panel version newer than the SDK supports.

## Recommended handling strategy

```python
from pasarguard_panel_api import (
    Pasarguard, PasarguardError,
    AuthorizationError, UserAlreadyExistsError, APIResponseError,
)

pg = Pasarguard(host, user, password)

try:
    user = pg.add_user(NewUser(username="alice", group_ids=[1]))
except UserAlreadyExistsError:
    print("already exists")
except AuthorizationError:
    print("bad credentials")
except APIResponseError:
    print("panel rejected the request")
except PasarguardError:
    print("some other SDK error")
except httpx.HTTPError:
    print("network problem")
```

Catch `PasarguardError` to handle all SDK-defined failures uniformly, and
`httpx.HTTPError` for connectivity issues.
