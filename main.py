import requests
from bs4 import BeautifulSoup
import os

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

RACE_ID = "202603187403"
URL = f"https://keirin.netkeiba.com/race/entry/?race_id={RACE_ID}"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://keirin.netkeiba.com/"
}


def scrape():

    session = requests.Session()
    session.headers.update(HEADERS)

    res = session.get(URL)
    print("status:", res.status_code)

    soup = BeautifulSoup(res.text, "html.parser")

    riders = []

    # 👇 出走表テーブルから取得（名前と得点）
    rows = soup.select("table.RaceTable01 tr")

    for r in rows:

        name = r.select_one(".Name")
        score = r.select_one(".Score")

        if not name or not score:
            continue

        name = name.text.strip()
        score = score.text.strip()

        riders.append((name, score))

    return riders


def send_discord(riders):

    msg = "🚴 出走表（名前＋得点）\n"

    for name, score in riders:
        msg += f"\n{name} ({score})"

    requests.post(WEBHOOK, json={"content": msg})


def main():

    riders = scrape()

    print("取得件数:", len(riders))

    if len(riders) == 0:
        print("データ取得失敗")
        return

    send_discord(riders)


if __name__ == "__main__":
    main()
