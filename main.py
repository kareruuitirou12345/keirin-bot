import requests
from bs4 import BeautifulSoup
import os

# GitHub Secretsに登録したWebhook
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]


def scrape_races():

    url = "https://keirin-station.com/keirindb/race/member/31/20260316/5/"  # 出走表URL

    res = requests.get(url)
    res.encoding = "utf-8"

    soup = BeautifulSoup(res.text, "html.parser")

    races = []

    # 例：レースごとのブロック
    race_blocks = soup.select(".race")

    for race in race_blocks:

        race_name = race.select_one(".race-title").text.strip()

        riders = race.select(".rider")

        scores = []
        styles = []

        for r in riders:

            score = float(r.select_one(".score").text)
            style = r.select_one(".style").text

            scores.append(score)
            styles.append(style)

        races.append({
            "name": race_name,
            "scores": scores,
            "styles": styles
        })

    return races


def is_chaos_race(race):

    scores = race["scores"]
    styles = race["styles"]

    score_diff = max(scores) - min(scores)

    escape_count = styles.count("逃")

    score = 0

    # 得点差小
    if score_diff <= 3:
        score += 3

    # 先行不在
    if escape_count == 0:
        score += 4

    return score >= 5


def send_discord(message):

    requests.post(
        DISCORD_WEBHOOK,
        json={"content": message}
    )


def main():

    races = scrape_races()

    chaos_races = []

    for race in races:

        if is_chaos_race(race):
            chaos_races.append(race["name"])

    if not chaos_races:
        print("荒れレースなし")
        return

    msg = "🔥荒れそうなレース\n"

    for r in chaos_races:
        msg += f"\n{r}"

    send_discord(msg)


if __name__ == "__main__":
    main()
