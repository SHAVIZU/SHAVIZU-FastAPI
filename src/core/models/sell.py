from sqlalchemy import Column, BIGINT, INTEGER, SMALLINT, DATETIME

from src.core.models import Base


class Tbl_sell(Base):
    __tablename__ = "tbl_sell"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    shop_id = Column(BIGINT, nullable=False)
    item_id = Column(BIGINT, nullable=False)
    price = Column(INTEGER, nullable=False)
    discount_rate = Column(SMALLINT)
    discount_price = Column(INTEGER)
    created_at = Column(DATETIME)
