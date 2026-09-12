import requests
from datetime import date, timedelta

ACCOUNT_NUMBER = "01491048088"
ENTITY_CODE = "SK"


def _current_week():
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday.isoformat(), sunday.isoformat()


def check_payment(nick):
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
            return False

        data = r.json()

        for t in data.get("iHubResponseInfo", []):
            text = (t.get("counterParty", "") + " " +
                    t.get("transactionDetails", ""))

            if nick.lower() in text.lower():
                return True

        return False

    except Exception:
        return False
