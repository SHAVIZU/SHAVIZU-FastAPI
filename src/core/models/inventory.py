from sqlalchemy import Column, BIGINT

from src.core.models import Base


class Tbl_inventory(Base):
    __tablename__ = "tbl_inventory"

    sell_id = Column(BIGINT, primary_key=True)
    item_size_id = Column(BIGINT, primary_key=True)
    amount = Column(BIGINT, nullable=False)
