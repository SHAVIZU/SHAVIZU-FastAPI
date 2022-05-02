from fastapi import APIRouter, status, Depends

from src import Settings, get_settings

from src.core.models import session_scope

from src.utils.shop import get_shop_information


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
def shop_information(shop_id: int, settings: Settings = Depends(get_settings)):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_shop_information(session=session, shop_id=shop_id)

        return response
