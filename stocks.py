from bs4 import BeautifulSoup
import requests

def scrap_stock_data(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    def get_value(field):
        tag = soup.find("fin-streamer", {"data-field": field})
        if tag:
            return float(tag.text.replace(',', '').replace('%', ''))
        return None

    return {
        "current_price": get_value("regularMarketPrice"),
        "price_change": get_value("regularMarketChange"),
        "percentage_change": get_value("regularMarketChangePercent"),
    }