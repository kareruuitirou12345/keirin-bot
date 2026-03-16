import requests
from bs4 import BeautifulSoup

url = "https://keirin-station.com/keirindb/race/member/31/20260316/5/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}

res = requests.get(url, headers=headers)

print(res.status_code)
print(res.text[:1000])
