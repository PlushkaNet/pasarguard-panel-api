# 🔑 Authentication

The SDK handles authentication for you. Understanding the flow helps you use
it correctly and debug issues.

## How it works

### 1. Token acquisition

Authentication requests an OAuth2-style access token from the panel:

```
POST /api/admin/token
Content-Type: application/x-www-form-urlencoded

grant_type=password
username=<admin user>
password=<admin password>
```

On success (`HTTP 200`), the token is extracted from the JSON response
(`access_token`) and stored on the client instance for the rest of its life.

On failure, `AuthorizationError` is raised with the status code and response
body.

### 2. Authenticated requests

All API calls send:

```
Authorization: Bearer <access_token>
```

### 3. Automatic (re-)authentication

The flow inside every public method is:

1. **Lazy login** — if no token is stored yet, authenticate first. This is
   why calling `auth()` explicitly is optional.
2. **Request** — send the request with the current token.
3. **Renewal** — if the panel answers `401` (expired or invalidated token),
   re-authenticate and retry the request **exactly once**.

This gives you the "token autorenew" feature: long-running processes never
fail because the token expired.

## When to call `auth()` explicitly

- You want **fail-fast** behavior: validate credentials at startup instead of
  discovering the problem on the first real request.
- You want a clear error before any other API call.

```python
pg = Pasarguard(host, user, password)
try:
    pg.auth()
except AuthorizationError:
    sys.exit("Bad credentials")
```

## Token lifecycle

- Tokens are stored **in memory only**, per client instance. Nothing is
  persisted to disk.
- There is no background refresh — renewal is triggered by a `401` response
  on the fly.
- A new `Pasarguard` instance starts with no token and logs in again.

## Security notes

- Credentials are stored on the client as given — don't hardcode them; read
  from environment variables, secrets managers, or config files.
- The panel connection uses whatever `httpx` does with your URL — use `https://`
  for anything outside a trusted network.
- Never log the client object or its attributes: it holds the password.
