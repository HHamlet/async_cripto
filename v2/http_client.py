import json
from json import JSONDecodeError

from aiohttp import ClientSession, ClientError
from v2.config import settings
import redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


class HTTPClient:
    def __init__(self, base_url: str, api_key: str):
        self._session = ClientSession(
            base_url=base_url,
            headers={
                "accept": "application/json",
                "x-cg-pro-api-key": api_key
            }
        )


class CGMHTTPClient(HTTPClient):
    async def get_coin_list(self):
        cache_name = "coins-list"
        coin_list_result = redis_client.get(cache_name)
        if coin_list_result is None:
            try:
                async with self._session.get("/api/v3/coins/markets?vs_currency=usd") as resp:
                    resp.raise_for_status()
                    result = await resp.json()
                    redis_client.set(cache_name, json.dumps(result), ex=120)
            except (ClientError, JSONDecodeError, TimeoutError) as e:
                print(f"Error fetching coin list: {e}")
                result = []
        else:
            result = json.loads(coin_list_result)
        return result

    async def get_coin(self, coin_id: str):
        cache_name = f"coins {coin_id}"
        coin_result = redis_client.get(cache_name)
        if coin_result is None:
            try:
                async with self._session.get(f"/api/v3/coins/{coin_id}") as resp:
                    resp.raise_for_status()
                    result = await resp.json()
                    redis_client.set(cache_name, json.dumps(result), ex=120)
            except (ClientError, JSONDecodeError, TimeoutError) as e:
                print(f"Error fetching coin {coin_id}: {e}")
                result = {}
        else:
            result = json.loads(coin_result)
        return result


cgm_client = CGMHTTPClient(
    base_url="https://api.coingecko.com",
    api_key=settings.CGM_API_KEY
)
