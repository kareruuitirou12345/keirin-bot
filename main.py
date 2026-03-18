import requests
from bs4 import BeautifulSoup
import os

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

RACE_ID = "202603187403"
URL = f"https://keirin.netkeiba.com/race/entry/?race_id={RACE_ID}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://keirin.netkeiba.com/",
    "Accept-Language": "ja-JP,ja;q=0.9"
}


def scrape():

    session = requests.Session()
    session.headers.update(HEADERS)

    res = session.get(URL)

    print("status:", res.status_code)
    print(res.text[:500])  # ←デバッグ

    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("table.RaceTable01 tr")

    riders = []

    for r in rows:

        number = r.select_one(".Umaban")
        name = r.select_one(".Name")
        score = r.select_one(".Score")

        if not number or not name:
            continue

        n = number.text.strip()
        nm = name.text.strip()
        sc = score.text.strip() if score else "-"

        riders.append((n, nm, sc))

    return riders


def send_discord(riders):

    msg = "🚴 出走表\n"

    for n, nm, sc in riders:
        msg += f"\n{n} {nm} ({sc})"

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
