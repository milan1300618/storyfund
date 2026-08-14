
import requests
from datetime import datetime, timedelta

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Zadaj nick, ktorý chceš hľadať
hladany_nick = "reklamacia"

# Výpočet obdobia: pondelok 00:01 -> nedeľa 16:00 aktuálneho týždňa
now = datetime.now()

monday = (now - timedelta(days=now.weekday())).replace(
    hour=0, minute=1, second=0, microsecond=0
)
sunday = monday + timedelta(days=6)
sunday = sunday.replace(hour=16, minute=0, second=0, microsecond=0)

params = {
    "accountNumber": "01491048088",
    "entityCode": "SK",
    "dateFrom": monday.strftime("%Y-%m-%d"),
    "dateTo": sunday.strftime("%Y-%m-%d"),
    "pageNumber": 1
}

r = requests.get(
    "https://www.unicreditbank.sk/show.pws.transparentTransactions.html",
    headers=headers,
    params=params,
    timeout=10
)

if r.status_code == 200:
    data = r.json()

    nasiel = False

    for t in data.get("iHubResponseInfo", []):
        poznamka = t.get("transactionDetails", "")

        if hladany_nick.lower() in poznamka.lower():
            print("Nick nájdený.")
            print("Dátum:", t.get("transactionDate"))
            print("Poznámka:", poznamka)
            nasiel = True
            break

    if not nasiel:
        print("Nick sa nenašiel.")
else:
    print("HTTP chyba:", r.status_code)
