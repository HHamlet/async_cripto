from fastapi import APIRouter
from v1.http_client import cripto_data
router = APIRouter(prefix="/cryptocurrencies")


@router.get("")
async def get_cryptocurrencies():
    return await cripto_data()


@router.get("/{currency_id}")
async def get_cryptocurrency(currency_id: str):
    data = await cripto_data()
    return data[currency_id]
