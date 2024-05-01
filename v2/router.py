from fastapi import APIRouter
from v2.http_client import cgm_client
router = APIRouter(prefix="/cryptocurrencies")


@router.get("")
async def get_coin_list():
    return await cgm_client.get_coin_list()


@router.get("/{coin_id}")
async def get_coin(coin_id: str):
    return await cgm_client.get_coin(coin_id)
