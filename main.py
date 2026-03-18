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
    print("length:", len(res.text))

    soup = BeautifulSoup(res.text, "html.parser")

    riders = []

    # 👇 全行を見る（決め打ちしない）
    for r in soup.find_all("tr"):

        text = r.get_text(" ", strip=True)

        # 👇 名前っぽい＋得点っぽい行を検出
        # 得点は「80.00」みたいな形式
        score_match = re.search(r"\d{2}\.\d{2}", text)

        if not score_match:
            continue

        score = score_match.group()

        # 👇 名前（日本語2〜4文字）を抽出
        name_match = re.search(r"[一-龥]{2,4}", text)

        if not name_match:
            continue

        name = name_match.group()

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
    print(riders)

    if len(riders) == 0:
        print("データ取得失敗")
        return

    send_discord(riders)


if __name__ == "__main__":
    main()
