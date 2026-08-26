# ======================================
# StoryFund - Firebase database.py
# ======================================

import json
import urllib.request
import urllib.error
import ssl
import certifi

from firebase_auth import get_id_token

FIREBASE_URL = "https://storyfund-59e53-default-rtdb.europe-west1.firebasedatabase.app"

SSL_CONTEXT = ssl.create_default_context(
    cafile=certifi.where()
)

DEFAULTS = {
    "users": [],
    "stories": [],
    "archive": [],
    "state": {
        "cycle_id": 1,
        "year": 0,
        "week": 0,
        "fund": 0,
        "status": "open"
    }
}


def _url(path):
    url = f"{FIREBASE_URL}/{path.strip('/')}.json"

    token = get_id_token()

    if token:
        from urllib.parse import quote
        url += "?auth=" + quote(token, safe="")

    return url


def _request(path, method="GET", data=None):
    body = None
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")

    request = urllib.request.Request(
        _url(path),
        data=body,
        headers={"Content-Type": "application/json"},
        method=method
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=15,
            context=SSL_CONTEXT
        ) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else None

    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Firebase chyba HTTP {e.code}: {detail}")

    except Exception as e:
        raise RuntimeError(f"Firebase chyba: {e}")


def _load(path, default):
    data = _request(path)
    if data is None:
        _save(path, default)
        return default
    return data


def _save(path, data):
    _request(path, method="PUT", data=data)


def get_users():
    return _load("users", [])


def save_users(data):
    _save("users", data)


def get_stories():
    return _load("stories", [])


def save_stories(data):
    _save("stories", data)


def clear_stories():
    _save("stories", [])


def get_archive():
    return _load("archive", [])


def save_archive(data):
    _save("archive", data)


def get_state():
    return _load("state", DEFAULTS["state"].copy())


def save_state(data):
    _save("state", data)
