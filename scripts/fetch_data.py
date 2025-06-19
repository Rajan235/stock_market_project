import requests
from config import API_KEY

def fetch_data(stock_name):
    url = f"https://stock.indianapi.in/historical_stats?stock_name={stock_name}&stats=all"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {stock_name}: {response.status_code}")
        return None

