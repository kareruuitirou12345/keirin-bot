import requests
from bs4 import BeautifulSoup

url = "https://keirin.netkeiba.com/race/entry/?race_id=202603163108"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)

soup = BeautifulSoup(res.text, "html.parser")

rows = soup.select("table.RaceTable01 tbody tr")

print("row count:", len(rows))

for row in rows:

    name = row.select_one(".Name")

    if name:
        print(name.text.strip())
