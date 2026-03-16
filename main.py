import requests

url = "https://keirin-station.com/keirindb/race/member/31/20260316/5/"
res = requests.get(url)

print(res.status_code)
print(res.text[:2000])
