import requests
from bs4 import BeautifulSoup
import os

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

url = "https://keirin.netkeiba.com/race/entry/?race_id=202603163108"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)

soup = BeautifulSoup(res.text, "html.parser")

rows = soup.select(".RaceTable01 tbody tr")

msg = "🚴 出走表\n"

for row in rows:

    number = row.select_one(".Umaban").text.strip()
    name = row.select_one(".Name").text.strip()
    score = row.select_one(".Score").text.strip()

    msg += f"\n{number} {name} ({score})"

requests.post(
    WEBHOOK,
    json={"content": msg}
)
