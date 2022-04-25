from sqlalchemy import Column, BIGINT, VARCHAR, DECIMAL

from src.core.models import Base


class Tbl_shop_information(Base):
    __tablename__ = "tbl_shop_information"

    shop_id = Column(BIGINT, primary_key=True)
    telephone = Column(VARCHAR(11), nullable=False)
    opening_hours = Column(VARCHAR(200), nullable=False)
    description = Column(VARCHAR(150))
    address = Column(VARCHAR(100), nullable=False)
    detailed_address = Column(VARCHAR(50), nullable=False)
    latitude = Column(DECIMAL(10, 8), nullable=False)
    longitude = Column(DECIMAL(11, 8), nullable=False)
