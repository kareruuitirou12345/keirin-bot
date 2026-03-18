import requests
from bs4 import BeautifulSoup
import os

URL = "https://keirinfrontier.jp/race-detail/20260318/31/2/"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scrape():
    res = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    riders = []

    rows = soup.select("table tr")

    for row in rows:
        tds = row.find_all("td")

        # 列数で判定（データ行だけ拾う）
        if len(tds) < 5:
            continue

        # 名前（リンク内）
        name_tag = row.select_one("a")
        if not name_tag:
            continue

        name = name_tag.text.strip()

        # 得点（画像的に3〜4列目あたり）
        try:
            score = tds[2].text.strip()
            float(score)  # 数値チェック
        except:
            continue

        riders.append((name, score))

    return riders


def send_discord(riders):
    msg = "🚴 出走表（名前＋得点）\n"

    for name, score in riders:
        msg += f"\n{name} ({score})"

    requests.post(WEBHOOK, json={"content": msg})


def main():
    riders = scrape()

    print("取得:", riders)

    if not riders:
        print("取得失敗")
        return

    send_discord(riders)


if __name__ == "__main__":
    main()
