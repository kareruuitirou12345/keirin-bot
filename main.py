import requests
from bs4 import BeautifulSoup
import os

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

RACE_ID = "202603163108"

url = f"https://keirin.netkeiba.com/race/entry/?race_id={RACE_ID}"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://keirin.netkeiba.com/"
}


def scrape():

    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("table.RaceTable01 tr")

    riders = []

    for r in rows:

        cols = r.find_all("td")

        if len(cols) < 7:
            continue

        number = cols[1].text.strip()
        name = cols[3].text.strip()
        score = cols[6].text.strip()

        riders.append((number, name, score))

    return riders


def send_discord(riders):

    msg = "🚴 出走表\n"

    for n, name, score in riders:
        msg += f"\n{n} {name} ({score})"

    requests.post(
        WEBHOOK,
        json={"content": msg}
    )


def main():

    riders = scrape()

    print("取得人数:", len(riders))

    if len(riders) == 0:
        print("データ取得失敗")
        return

    send_discord(riders)


if __name__ == "__main__":
    main()
