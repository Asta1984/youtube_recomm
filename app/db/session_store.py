# In-memory store — swap this for Redis or a DB in production
# Structure: { "state": ..., "code_verifier": ..., "token": ..., "refresh_token": ... }

_store: dict = {}


def get(key: str):
    return _store.get(key)


def set(key: str, value: str):
    _store[key] = value


def clear():
    _store.clear()


def all() -> dict:
    return _store