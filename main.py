import requests

url = "https://keirin-station.com/keirindb/race/member/31/20260316/5/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://keirin-station.com/",
}

res = requests.get(url, headers=headers)

print(res.status_code)
print(res.text[:1000])
