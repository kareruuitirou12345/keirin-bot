import requests
import os

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

requests.post(
    WEBHOOK,
    json={"content": "テスト通知"}
)
