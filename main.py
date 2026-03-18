import requests
from bs4 import BeautifulSoup
import os
import re

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
    print("html length:", len(res.text))

    soup = BeautifulSoup(res.text, "html.parser")

    riders = []
    seen = set()

    # 👇 全行を走査
    for row in soup.find_all("tr"):

        cols = row.find_all("td")

        if len(cols) < 5:
            continue

        # 👇 名前（aタグ）を優先取得
        name_tag = row.find("a")
        if not name_tag:
            continue

        name = name_tag.text.strip()

        # 👇 得点（85.00みたいな数値）を探す
        score = None
        for c in cols:
            txt = c.text.strip()
            if re.match(r"^\d{2}\.\d{2}$", txt):
                score = txt
                break

        if not score:
            continue

        key = (name, score)

        # 👇 重複排除
        if key in seen:
            continue

        seen.add(key)
        riders.append(key)

    return riders


def send_discord(riders):

    msg = "🚴 出走表（名前＋得点）\n"

    for name, score in riders:
        msg += f"\n{name} ({score})"

    requests.post(WEBHOOK, json={"content": msg})


def main():

    riders = scrape()

    print("取得件数:", len(riders))
    print(riders)

    if len(riders) == 0:
        print("データ取得失敗")
        return

    send_discord(riders)


if __name__ == "__main__":
    main()
