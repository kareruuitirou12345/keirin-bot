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

    res = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("table.RaceTable01 tr")

    riders = []

    for r in rows:

        number = r.select_one(".Umaban")
        name = r.select_one(".Name")
        score = r.select_one(".Score")

        # ←ここが重要（cols使わない）
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

    requests.post(
        WEBHOOK,
        json={"content": msg}
    )


def main():

    riders = scrape()

    print("取得件数:", len(riders))

    if len(riders) == 0:
        print("データ取得失敗")
        return

    send_discord(riders)


if __name__ == "__main__":
    main()
