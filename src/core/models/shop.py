from sqlalchemy import Column, BIGINT, VARCHAR, CHAR, DATETIME

from src.core.models import Base


class Tbl_shop(Base):
    __tablename__ = "tbl_shop"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(VARCHAR(12), nullable=False)
    password = Column(CHAR(60), nullable=False)
    created_at = Column(DATETIME, nullable=False)
    registration_number = Column(VARCHAR(12), nullable=False)
    boss_name = Column(VARCHAR(10), nullable=False)
    name = Column(VARCHAR(45), nullable=False)
