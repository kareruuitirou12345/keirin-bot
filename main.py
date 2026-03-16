import requests

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://keirin-station.com/"
})

url = "https://keirin-station.com/keirindb/race/member/31/20260316/5/"

res = session.get(url)

print(res.status_code)
