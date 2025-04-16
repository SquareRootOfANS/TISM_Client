import requests

url = "https://sc-trade.tools/api/crowdsource/commodity-listings"
headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    print("[Status Code]:", response.status_code)
    print("[Content]:", response.text[:300])  # just a preview
except Exception as e:
    print("Error:", e)
