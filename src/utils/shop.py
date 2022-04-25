from sqlalchemy import literal_column
from sqlalchemy.orm import Session

from src.core.models.shop import Tbl_shop
from src.core.models.shop_information import Tbl_shop_information
from src.core.models.shop_image import Tbl_shop_image


def get_shop_information(session: Session, shop_id: int):
    shop_info = session.query(
        Tbl_shop.name,
        Tbl_shop_information.address,
        Tbl_shop_information.detailed_address,
        Tbl_shop_information.telephone,
        Tbl_shop_information.opening_hours,
        Tbl_shop_information.description,
        literal_column("group_concat(tbl_shop_image.image_url ORDER BY tbl_shop_image.sequence SEPARATOR ' ') AS genre")
    )\
        .join(Tbl_shop_information, Tbl_shop.id == Tbl_shop_information.shop_id)\
        .join(Tbl_shop_image, Tbl_shop.id == Tbl_shop_image.shop_id)\
        .filter(Tbl_shop.id == shop_id)\
        .first()

    return {
        "name": shop_info["name"],
        "address": f'{shop_info["address"]} {shop_info["detailed_address"]}',
        "telephone": shop_info["telephone"],
        "opening_hours": shop_info["opening_hours"],
        "description": shop_info["description"],
        "images": shop_info["genre"].split()
    }
