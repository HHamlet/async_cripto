import json
from decimal import Decimal
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import redis

url = 'https://www.coingecko.com'

headers = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'
}
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


def refine_price(text):
    return text.strip(' \n$').replace(",", "")


async def cripto_data():
    cache_name = "coin_data"
    coin_data_result = redis_client.get(cache_name)
    if coin_data_result is None:
        coin_data = {}  # Define coin_data here
        async with ClientSession() as session:
            async with session.get('https://www.coingecko.com', headers=headers) as response:
                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                coins = soup.find('tbody').find_all('tr')
                for coin in coins:
                    teg_td = coin.find_all('td', class_=lambda x: x and 'tw-hidden' not in x.split())
                    coin_rank = teg_td[1].text.strip()
                    coin_name_tk = teg_td[2].div.text.split()
                    coin_link = url + teg_td[2].a.get('href')
                    coin_img = teg_td[2].img.get('src')
                    decimal_price = Decimal(refine_price(teg_td[4].text))
                    decimal_volume24h = Decimal(refine_price(teg_td[9].text))
                    decimal_market_cap = Decimal(refine_price(teg_td[10].text))
                    coin_data[coin_rank] = {
                        "coin_name": coin_name_tk[0],
                        "coin_name_tk": coin_name_tk[1],
                        "coin_link": coin_link,
                        "coin_img": coin_img,
                        "price": str(decimal_price),
                        "volume24h": str(decimal_volume24h),
                        "market_cap": str(decimal_market_cap)
                    }
                redis_client.set(cache_name, json.dumps(coin_data), 60)
    else:
        coin_data = json.loads(coin_data_result)
    return coin_data
