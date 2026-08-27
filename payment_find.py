import requests
from datetime import date, timedelta

ACCOUNT_NUMBER = "01491048088"
ENTITY_CODE = "SK"

TEST_ALL_TRANSACTIONS = False  # False = iba aktuálny týždeň


def _current_week():
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday.isoformat(), sunday.isoformat()


def find_payment(nick):
    if TEST_ALL_TRANSACTIONS:
        date_from = "2025-01-01"
        date_to = "2030-12-31"
    else:
        date_from, date_to = _current_week()

    headers = {"User-Agent": "Mozilla/5.0"}
    params = {
        "accountNumber": ACCOUNT_NUMBER,
        "entityCode": ENTITY_CODE,
        "dateFrom": date_from,
        "dateTo": date_to,
        "pageNumber": 1,
    }

    try:
        r = requests.get(
            "https://www.unicreditbank.sk/show.pws.transparentTransactions.html",
            headers=headers,
            params=params,
            timeout=10,
        )

        if r.status_code != 200:
            return None

        data = r.json()

        # NIK má tvar SF + 5 číslic.
        # Do platby sa zadáva iba 5-ciferné číslo ako VS.
        search_number = nick.strip()

        if search_number.upper().startswith("SF"):
            search_number = search_number[2:]

        search_number = search_number.strip()

        # Hľadáme presnú zhodu iba vo Variabilnom symbole.
        for t in data.get("iHubResponseInfo", []):

            variable_code = str(
                t.get("variableCode", "")
            ).strip()

            if variable_code == search_number:
                return t

        return None

    except Exception:
        return None


if __name__ == "__main__":
    nick = input("Nick: ").strip()
    import json

    result = find_payment(nick)

    if result is None:
        print("Platba nebola nájdená.")
    else:
        print("\n=== KĽÚČE ===")
        print(list(result.keys()))

        print("\n=== CELÁ TRANSAKCIA ===")
        print(json.dumps(result, indent=4, ensure_ascii=False))
