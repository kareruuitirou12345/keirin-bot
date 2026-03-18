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

    rows = soup.select("table tr")

    for r in rows:

        cols = r.find_all("td")

        # 👇このページの構造に合わせる
        if len(cols) >= 10:

            try:
                # 名前（aタグ）
                name_tag = cols[3].find("a")
                if not name_tag:
                    continue

                name = name_tag.text.strip()

                # 競走得点（固定位置）
                score = cols[4].text.strip()

                riders.append((name, score))

            except:
                continue

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
