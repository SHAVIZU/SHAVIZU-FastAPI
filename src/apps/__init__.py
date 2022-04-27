from fastapi import APIRouter

from src.apps import product, search, shop

api_router = APIRouter()
api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(shop.router, prefix="/shop", tags=["shop"])
