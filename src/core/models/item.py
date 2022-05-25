from sqlalchemy import Column, BIGINT, VARCHAR

from src.core.models import Base


class Tbl_item(Base):
    __tablename__ = "tbl_item"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50), nullable=False)
    style_code = Column(VARCHAR(20), nullable=False)
    category = Column(VARCHAR(10), nullable=False)
    image_url = Column(VARCHAR(225), nullable=False)
    brand_id = Column(BIGINT, nullable=False)
