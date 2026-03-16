import requests
from bs4 import BeautifulSoup
import os

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

# レースID
RACE_ID = "202603163108"

URL = f"https://keirin.netkeiba.com/race/entry/?race_id={RACE_ID}"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://keirin.netkeiba.com/"
}


def scrape_race():

    res = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("table.RaceTable01 tbody tr")

    riders = []

    for r in rows:

        number = r.select_one(".Umaban")
        name = r.select_one(".Name")
        score = r.select_one(".Score")

        if not number or not name:
            continue

        number = number.text.strip()
        name = name.text.strip()

        score_text = "-"
        if score:
            score_text = score.text.strip()

        riders.append({
            "number": number,
            "name": name,
            "score": score_text
        })

    return riders


def send_discord(riders):

    msg = "🚴 出走表\n"

    for r in riders:
        msg += f"\n{r['number']} {r['name']} ({r['score']})"

    requests.post(
        WEBHOOK,
        json={"content": msg}
    )


def main():

    riders = scrape_race()

    if not riders:
        print("データ取得失敗")
        return

    send_discord(riders)


if __name__ == "__main__":
    main()
