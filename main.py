import requests
from bs4 import BeautifulSoup

url = "https://keirin.netkeiba.com/race/entry/?race_id=202603163108"

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8",
    "Connection": "keep-alive",
    "Referer": "https://keirin.netkeiba.com/"
}

session.headers.update(headers)

res = session.get(url)

print(res.status_code)
print(res.text[:1000])

soup = BeautifulSoup(res.text, "html.parser")

rows = soup.select("table tr")

print("row count:", len(rows))
