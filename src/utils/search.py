from fastapi import HTTPException, status

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from src.core.models.item import Tbl_item
from src.core.models.brand import Tbl_brand
from src.core.models.shop import Tbl_shop
from src.core.models.shop_image import Tbl_shop_image
from src.core.models.shop_information import Tbl_shop_information
from src.core.models.sell import Tbl_sell
from src.core.models.item_size import Tbl_item_size
from src.core.models.inventory import Tbl_inventory



def get_item_search_result(session: Session, style_code: str, name: str, brand: str, category: list):
    query = session.query(
        Tbl_item.id,
        Tbl_item.image_url,
        Tbl_brand.name,
        Tbl_item.name,
        Tbl_item.style_code
    ).join(Tbl_brand, Tbl_item.brand_id == Tbl_brand.id)

    if not style_code:
        query = query.filter(Tbl_item.style_code == style_code)
    elif not name:
        query = query.filter(Tbl_item.name == name)
    elif not brand:
        query = query.filter(Tbl_brand.name == brand)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No keyword in query")

    if not category:
        query = query.filter(Tbl_item.category.in_(category))

    items = query.all()

    return [{
        "id": id,
        "image_url": image_url,
        "brand_name": brand_name,
        "item_name": item_name,
        "style_code": style_code_
    } for id, image_url, brand_name, item_name, style_code_ in items]


def get_item_search_detail(session: Session, item_id: int):
    shops = session.query(
        Tbl_shop.id,
        Tbl_shop.name,
        Tbl_shop_image.image_url,
        Tbl_shop_information.opening_hours,
        Tbl_shop_information.address,
        Tbl_shop_information.detailed_address,
        Tbl_sell.discount_price,
        func.group_concat(func.concat(Tbl_item_size.size, ";", Tbl_inventory.amount), "|").label("stock")
    )\
        .select_from(Tbl_shop)\
        .join(Tbl_shop_information, Tbl_shop.id == Tbl_shop_information.shop_id)\
        .join(Tbl_shop_image, and_(Tbl_shop.id == Tbl_shop_information.shop_id, Tbl_shop_image.sequence == 1))\
        .join(Tbl_sell, Tbl_shop.id == Tbl_sell.shop_id)\
        .join(Tbl_inventory, Tbl_sell.id == Tbl_inventory.sell_id)\
        .join(Tbl_item_size, Tbl_inventory.item_size_id == Tbl_item_size.id)\
        .filter(Tbl_sell.item_id == item_id)\
        .order_by(func.sum(Tbl_inventory.amount).desc()).all()

    return [{
        "id": id,
        "name": name,
        "image_url": image_url,
        "opening_hours": opening_hours,
        "address": f"{address} {detailed_address}",
        "inventory": [{
            "size": size,
            "amount": amount
        } for size, amount in map(lambda x: x.split(";"), stock.split("|")) ]
    } for id, name, image_url, opening_hours, address, detailed_address, price, stock in shops]


def get_shop_search_result(
        session: Session,
        max_latitude: float,
        max_longitude: float,
        min_latitude: float,
        min_longitude: float
):  # latitude: 위도, longitude: 경도
    shops = session.query(
        Tbl_shop.id,
        Tbl_shop.name,
        Tbl_shop_image.image_url,
        Tbl_shop_information.opening_hours,
        Tbl_shop_information.address,
        Tbl_shop_information.detailed_address,
        Tbl_shop_information.latitude,
        Tbl_shop_information.longitude
    )\
        .select_from(Tbl_shop)\
        .join(Tbl_shop_image, and_(Tbl_shop.id == Tbl_shop_information.shop_id, Tbl_shop_image.sequence == 1))\
        .join(Tbl_shop_information, Tbl_shop.id == Tbl_shop_information.shop_id)\
        .filter(Tbl_shop_information.latitude.between(min_latitude, max_latitude))\
        .filter(Tbl_shop_information.longitude.between(min_longitude, max_longitude))\
        .all()

    return [{
        "id": id,
        "name": name,
        "image_url": image_url,
        "opening_hours": opening_hours,
        "address": f"{address} {detailed_address}",
        "latitude": latitude,
        "longitude": longitude
    } for id, name, image_url, opening_hours, address, detailed_address, latitude, longitude in shops]
