from fastapi import APIRouter, status, Query, Depends

from typing import Optional

from src import Settings, get_settings
from src.core.models import session_scope

from src.utils.search import get_item_search_result, get_item_search_detail, get_shop_search_result


router = APIRouter()


@router.get("/item", status_code=status.HTTP_200_OK)
def search_item(
        style_code: Optional[str] = Query(None),
        name: Optional[str] = Query(None),
        brand: Optional[str] = Query(None),
        category: Optional[str] = Query(None),
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_item_search_result(
            session=session,
            style_code=style_code,
            name=name,
            brand=brand,
            category=category.split(",") if category else category
        )

        return response


@router.get("/item/detail", status_code=status.HTTP_200_OK)
def search_item_detail(item_id: int, settings: Settings = Depends(get_settings)):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_item_search_detail(session=session, item_id=item_id)

        return response


@router.get("/shop", status_code=status.HTTP_200_OK)
def search_shop(
        max_lat: float,
        max_lng: float,
        min_lat: float,
        min_lng: float,
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_shop_search_result(
            session=session,
            max_latitude=max_lat,
            max_longitude=max_lng,
            min_latitude=min_lat,
            min_longitude=min_lng
        )

        return response
