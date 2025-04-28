from requests_html import HTMLSession


session = HTMLSession()
term = "слон"
url = f"https://ruwordnet.ru/ru/search/{term}"
r = session.get(url)
r.html.render(sleep=2)

with open("rendered.html", "w", encoding="utf-8") as f:
    f.write(r.html.html)

print("[DEBUG] Rendered HTML сохранён в 'rendered.html'")
