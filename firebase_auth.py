# ======================================
# StoryFund - Firebase Authentication
# ======================================

import json
import urllib.request
import urllib.error


# Firebase Web API key z konfigurácie StoryFund web app.
FIREBASE_API_KEY = "AIzaSyBZieay3c8tiq1ihYfZcolTAkVJoCk21yE"

AUTH_URL = (
    "https://identitytoolkit.googleapis.com/v1/"
    "accounts:signInWithPassword"
)

SIGNUP_URL = (
    "https://identitytoolkit.googleapis.com/v1/"
    "accounts:signUp"
)


# Aktuálny Firebase ID token.
_current_id_token = None


def _auth_email(nik):
    # Interný identifikátor pre Firebase Authentication.
    # Nie je to skutočný e-mail.
    return nik.strip() + "@storyfund.local"


def _post_auth(url, payload):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return {
                "ok": True,
                "data": json.loads(
                    response.read().decode("utf-8")
                )
            }

    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(
                e.read().decode("utf-8")
            )
        except Exception:
            detail = {}

        return {
            "ok": False,
            "error": detail
        }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }


def create_user_auth(nik, pin):
    """Vytvorí Firebase Authentication účet pre účastníka."""

    email = _auth_email(nik)

    payload = {
        "email": email,
        "password": pin,
        "returnSecureToken": True
    }

    url = f"{SIGNUP_URL}?key={FIREBASE_API_KEY}"

    result = _post_auth(url, payload)

    if not result["ok"]:
        return result

    data = result["data"]

    return {
        "ok": True,
        "localId": data.get("localId"),
        "idToken": data.get("idToken"),
        "refreshToken": data.get("refreshToken")
    }


def login_user_auth(nik, pin):
    """Prihlási účastníka do Firebase Authentication."""

    global _current_id_token

    email = _auth_email(nik)

    payload = {
        "email": email,
        "password": pin,
        "returnSecureToken": True
    }

    url = f"{AUTH_URL}?key={FIREBASE_API_KEY}"

    result = _post_auth(url, payload)

    if not result["ok"]:
        _current_id_token = None
        return result

    data = result["data"]

    _current_id_token = data.get("idToken")

    return {
        "ok": True,
        "localId": data.get("localId"),
        "idToken": data.get("idToken"),
        "refreshToken": data.get("refreshToken")
    }


def get_id_token():
    """Vráti aktuálny Firebase ID token."""

    return _current_id_token


def clear_id_token():
    """Vymaže aktuálny Firebase ID token."""

    global _current_id_token
    _current_id_token = None


def login_admin(email, password):
    """Overí admina cez Firebase Authentication."""

    global _current_id_token

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    url = f"{AUTH_URL}?key={FIREBASE_API_KEY}"

    result = _post_auth(url, payload)

    if not result["ok"]:
        _current_id_token = None
        return False

    data = result["data"]

    _current_id_token = data.get("idToken")

    return bool(_current_id_token)
