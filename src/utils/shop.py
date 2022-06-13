from fastapi import HTTPException, status

from sqlalchemy import literal_column, and_, func
from sqlalchemy.orm import Session

from src.core.models.shop import Tbl_shop
from src.core.models.shop_information import Tbl_shop_information
from src.core.models.shop_image import Tbl_shop_image
from src.core.models.sell import Tbl_sell
from src.core.models.item import Tbl_item
from src.core.models.brand import Tbl_brand
from src.core.models.item_size import Tbl_item_size
from src.core.models.inventory import Tbl_inventory


def is_shop(session: Session, shop_id: int):
    return session.query(Tbl_shop).filter(Tbl_shop.id == shop_id).scalar()


def get_shop_information(session: Session, shop_id: int):
    if not is_shop(session=session, shop_id=shop_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no such shop")

    shop_info = session.query(
        Tbl_shop.name,
        Tbl_shop_information.address,
        Tbl_shop_information.detailed_address,
        Tbl_shop_information.telephone,
        Tbl_shop_information.opening_hours,
        Tbl_shop_information.description,
        literal_column("group_concat(tbl_shop_image.image_url ORDER BY tbl_shop_image.sequence SEPARATOR ' ') AS image_urls")
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
        "images": shop_info["image_urls"].split()
    }


def get_shop_name(session: Session, shop_id):
    return session.query(Tbl_shop.name).filter(Tbl_shop.id == shop_id).first()["name"]


def get_shop_items(session: Session, shop_id: int, brand: list, category: list, size: list):
    if not is_shop(session=session, shop_id=shop_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no such shop")

    query = session.query(
        Tbl_sell.discount_price,
        Tbl_sell.discount_rate,
        Tbl_item.name.label("item_name"),
        Tbl_item.image_url,
        Tbl_brand.name.label("brand_name"),
        func.group_concat(func.concat(Tbl_item_size.size, ";", Tbl_inventory.amount), "|").label("stock")
    )\
        .join(Tbl_item, Tbl_sell.item_id == Tbl_item.id)\
        .join(Tbl_brand, Tbl_item.brand_id == Tbl_brand.id)\
        .join(Tbl_item_size, Tbl_item.id == Tbl_item_size.item_id)\
        .join(Tbl_inventory, and_(Tbl_sell.id == Tbl_inventory.sell_id, Tbl_item_size.id == Tbl_inventory.item_size_id))\
        .filter(Tbl_sell.shop_id == shop_id)

    if brand:
        query = query.filter(Tbl_brand.name.in_(brand))
    if category:
        query = query.filter(Tbl_item.category.in_(category))
    if size:
        query = query.filter(Tbl_item_size.size.in_(size))

    items = query.order_by(Tbl_sell.created_at.desc(), Tbl_inventory.amount.desc())

    return {
        "shop_name": get_shop_name(session=session, shop_id=shop_id),
        "items": [{
            "discount_price": discount_price,
            "discount_rate": discount_rate,
            "item_name": item_name,
            "image_url": image_url,
            "brand_name": brand_name,
            "inventory": [{
                "size": size_,
                "amount": amount
            } for size_, amount in map(lambda x: x.split(";"), stock.split("|")) ]
        } for discount_price, discount_rate, item_name, image_url, brand_name, stock in items.all() if items.scalar()]
    }


def get_shop_brands(session: Session, shop_id: int):
    if not is_shop(session=session, shop_id=shop_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no such shop")

    brands = session.query(Tbl_brand.name)\
        .distinct(Tbl_brand.name)\
        .join(Tbl_item, Tbl_brand.id == Tbl_item.brand_id)\
        .join(Tbl_sell, Tbl_item.id == Tbl_sell.item_id)\
        .filter(Tbl_sell.shop_id == shop_id).all()

    return {
        "brands": [brand["name"] for brand in brands]
    }


def get_shop_item_sizes(session: Session, shop_id: int, categories: list):
    if not is_shop(session=session, shop_id=shop_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no such shop")

    sizes = session.query(
        Tbl_item_size.size
    )\
        .distinct(Tbl_item_size.size)\
        .join(Tbl_item, Tbl_item_size.item_id == Tbl_item.id)\
        .join(Tbl_sell, Tbl_item.id == Tbl_sell.item_id)\
        .filter(and_(Tbl_sell.shop_id == shop_id, Tbl_item.category.in_(categories if categories else [])))\
        .all()

    return {
        "sizes": [size["size"] for size in sizes]
    }
