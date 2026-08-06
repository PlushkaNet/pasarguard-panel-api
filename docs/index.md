# 📖 pasarguard-panel-api documentation

Sync & async Python SDK for the [Pasarguard](https://github.com/PasarGuard/panel) panel API.

## Getting started

- **[Quick start](quickstart.md)** — install, first steps, sync vs async
- **[Authentication](authentication.md)** — how tokens are obtained, renewed and handled automatically

## Reference

- **[API reference](api-reference.md)** — all client methods (`Pasarguard` / `AsyncPasarguard`)
- **[Models reference](models.md)** — Pydantic models returned by the API
- **[Enums](models.md#enums)** — `Status` enum values
- **[Errors](errors.md)** — exception hierarchy and how to handle failures

## Project layout

```
pasarguard-panel-api/
├── pasarguard_panel_api/
│   ├── __init__.py      # public exports, version
│   ├── sync.py          # Pasarguard (sync client)
│   ├── asyncio.py       # AsyncPasarguard (async client)
│   ├── models.py        # Pydantic response/request models
│   ├── enums.py         # Status enum
│   ├── exceptions.py    # error hierarchy
│   └── py.typed         # PEP 561 marker for type checkers
├── examples/            # runnable usage examples
├── tests.py             # smoke tests (runnable directly)
└── pyproject.toml       # build config (hatchling), deps, metadata
```
