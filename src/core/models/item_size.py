from sqlalchemy import Column, BIGINT, VARCHAR

from src.core.models import Base


class Tbl_item_size(Base):
    __tablename__ = "tbl_item_size"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    item_id = Column(BIGINT, nullable=False)
    size = Column(VARCHAR(10), nullable=False)
