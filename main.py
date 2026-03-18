import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

URL = "https://keirinfrontier.jp/race-detail/20260318/31/2/"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]


def scrape():

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    driver.get(URL)

    time.sleep(5)  # ←JS読み込み待ち（重要）

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    riders = []

    rows = soup.select("table tr")

    for row in rows:
        tds = row.find_all("td")

        if len(tds) < 5:
            continue

        name = tds[1].text.strip()

        try:
            score = tds[2].text.strip()
            float(score)
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

    print(riders)

    if not riders:
        print("取得失敗")
        return

    send_discord(riders)


if __name__ == "__main__":
    main()
