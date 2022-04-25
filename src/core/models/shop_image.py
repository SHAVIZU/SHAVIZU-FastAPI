from sqlalchemy import Column, BIGINT, VARCHAR, INTEGER

from src.core.models import Base


class Tbl_shop_image(Base):
    __tablename__ = "tbl_shop_image"

    id = Column(BIGINT, primary_key=type, autoincrement=True)
    image_url = Column(VARCHAR(225), nullable=False)
    sequence = Column(INTEGER, nullable=False)
    shop_id = Column(BIGINT, nullable=False)
