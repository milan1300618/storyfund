from requests_html import HTMLSession

URL = "https://www.unicreditbank.sk/sk/ostatne/transparentny-ucet.html?IBAN=SK5611110000001491048088"

session = HTMLSession()

print("Načítavam stránku...")

r = session.get(URL)

print("Renderujem JavaScript...")

r.html.render(timeout=30, sleep=3)

print("Hotovo")

html = r.html.html

print("Dĺžka HTML:", len(html))

with open("rendered.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Uložené do rendered.html")