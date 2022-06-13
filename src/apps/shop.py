from fastapi import APIRouter, status, Depends, Query

from typing import Optional, List

from src import Settings, get_settings

from src.core.models import session_scope

from src.utils.shop import get_shop_information, get_shop_items, get_shop_brands, get_shop_item_sizes


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
def shop_information(shop_id: int, settings: Settings = Depends(get_settings)):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_shop_information(session=session, shop_id=shop_id)

        return response


@router.get("/items", status_code=status.HTTP_200_OK)
def shop_items(
        shop_id: int,
        brand: Optional[List[int]] = Query(None),
        category: Optional[List[str]] = Query(None),
        size: Optional[List[str]] = Query(None),
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_shop_items(
            session=session,
            shop_id=shop_id,
            brand=brand,
            category=category,
            size=size
        )

        return response


@router.get("/brands", status_code=status.HTTP_200_OK)
def shop_brands(shop_id: int, settings: Settings = Depends(get_settings)):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_shop_brands(session=session, shop_id=shop_id)

        return response


@router.get("/sizes", status_code=status.HTTP_200_OK)
def get_sizes(
        shop_id: int,
        category: Optional[List[str]] = Query(None),
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_shop_item_sizes(session=session, shop_id=shop_id, categories=category)

        return response
