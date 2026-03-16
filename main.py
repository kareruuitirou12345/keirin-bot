import requests
from bs4 import BeautifulSoup

url = "https://keirin.netkeiba.com/race/entry/?race_id=202603163108"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://keirin.netkeiba.com/",
}

session = requests.Session()
res = session.get(url, headers=headers)

print(res.status_code)

soup = BeautifulSoup(res.text, "html.parser")

rows = soup.select("table.RaceTable01 tr")

print("row count:", len(rows))

for r in rows:
    cols = r.find_all("td")
    if len(cols) > 3:
        number = cols[1].text.strip()
        name = cols[3].text.strip()
        print(number, name)
