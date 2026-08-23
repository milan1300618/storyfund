import json
import os
import config

SETTINGS_FILE = "settings.json"


def _default_settings():
    """Načíta všetky veľké premenné z config.py."""
    data = {}

    for key in dir(config):
        if key.isupper():
            data[key] = getattr(config, key)

    return data


def load_settings():
    """Načíta settings.json a doplní chýbajúce hodnoty z config.py."""

    defaults = _default_settings()

    if not os.path.exists(SETTINGS_FILE):
        save_settings(defaults)
        return defaults

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        settings = json.load(f)

    changed = False

    for key, value in defaults.items():
        if key not in settings:
            settings[key] = value
            changed = True

    if changed:
        save_settings(settings)

    return settings


def save_settings(settings):
    """Uloží nastavenia."""

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)


def get(key):
    """Vráti jednu hodnotu nastavenia."""

    settings = load_settings()
    return settings.get(key)


def set(key, value):
    """Zmení jednu hodnotu nastavenia."""

    settings = load_settings()
    settings[key] = value
    save_settings(settings)