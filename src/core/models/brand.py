from sqlalchemy import Column, BIGINT, VARCHAR

from src.core.models import Base


class Tbl_brand(Base):
    __tablename__ = "tbl_brand"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(30), nullable=False)
