# ======================================
# StoryFund v0.6
# File: balance.py
# Automatická aktualizácia zostatku
# ======================================

import time
import requests

from database import get_state, save_state


TRANSPARENT_ACCOUNTS_URL = (
    "https://www.unicreditbank.sk/show.pws.transparentAccounts.html"
)

ACCOUNT_IBAN = "SK5611110000001491048088"
ENTITY_CODE = "SK"

UPDATE_INTERVAL = 60 * 60  # 1 hodina


def _get_balance_from_unicredit():

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": (
            "https://www.unicreditbank.sk/sk/ostatne/"
            "transparentny-ucet.html?IBAN=" + ACCOUNT_IBAN
        ),
        "X-Requested-With": "XMLHttpRequest",
    }

    params = {
        "iban": ACCOUNT_IBAN,
        "entityCode": ENTITY_CODE,
        "pageNumber": 1,
    }

    r = requests.get(
        TRANSPARENT_ACCOUNTS_URL,
        params=params,
        headers=headers,
        timeout=15,
    )

    r.raise_for_status()

    data = r.json()

    accounts = data.get("iHubResponseInfo", [])

    if not accounts:
        raise RuntimeError(
            "UniCredit nevrátil údaje o účte."
        )

    balance = accounts[0].get("balance")

    if balance is None:
        raise RuntimeError(
            "UniCredit nevrátil zostatok účtu."
        )

    return float(balance)


def update_balance_if_needed():

    state = get_state()

    now = time.time()

    last_update = float(
        state.get("balance_updated_at", 0) or 0
    )

    # Ak bol zostatok aktualizovaný
    # počas poslednej hodiny, nič nerobíme.
    if last_update > 0:

        if (now - last_update) < UPDATE_INTERVAL:

            return float(
                state.get("fund", 0) or 0
            )

    try:

        balance = _get_balance_from_unicredit()

        state["fund"] = balance

        state["balance_updated_at"] = now

        save_state(state)

        print(
            "StoryFund: zostatok aktualizovaný:",
            f"{balance:.2f} EUR"
        )

        return balance

    except Exception as e:

        print(
            "StoryFund: aktualizácia zostatku zlyhala:",
            e
        )

        # Pri chybe necháme starú hodnotu.
        return float(
            state.get("fund", 0) or 0
        )