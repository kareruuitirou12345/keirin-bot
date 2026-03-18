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

    soup = BeautifulSoup(res.text, "html.parser")

    riders = []

    # 👇全trを走査して「列数」で判定（これが一番安定）
    for r in soup.select("tr"):

        cols = [c.text.strip() for c in r.find_all("td")]

        # 👇この条件が重要（画像の表）
        if len(cols) >= 13:

            try:
                score = cols[0]          # 競走得点
                style = cols[1]          # 脚質（逃・追・両）
                s_count = cols[2]        # S
                b_count = cols[3]        # B
                nige = cols[4]           # 逃げ
                makuri = cols[5]         # まくり
                sashi = cols[6]          # 差し

                win = cols[10]           # 勝率
                rentai = cols[11]        # 2連対率
                sanrentai = cols[12]     # 3連対率

                riders.append({
                    "score": score,
                    "style": style,
                    "win": win,
                    "2rentai": rentai,
                    "3rentai": sanrentai
                })

            except Exception as e:
                print("skip:", e)

    return riders


def send_discord(riders):

    msg = "🔥 成績テーブル\n"

    for r in riders:
        msg += (
            f"\n得点:{r['score']}"
            f" 脚質:{r['style']}"
            f" 勝率:{r['win']}"
            f" 2連:{r['2rentai']}"
            f" 3連:{r['3rentai']}"
        )

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
