import requests
from bs4 import BeautifulSoup
import os

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

def scrape():

    url = "https://example.com"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    races = []

    for r in soup.select(".race"):

        name = r.select_one(".race-name").text

        races.append(name)

    return races


def send_discord(msg):

    requests.post(
        WEBHOOK,
        json={"content": msg}
    )


def main():

    races = scrape()

    if not races:
        return

    message = "荒れそうなレース\n"

    for r in races:
        message += f"\n{r}"

    send_discord(message)


if __name__ == "__main__":
    main()
