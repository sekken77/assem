from datetime import datetime

from sqlalchemy import Column, String, DateTime

from db import Base


class Sample(Base):
    __tablename__ = 'sample'

    id = Column("id", String(255), unique=True, primary_key=True, nullable=False)
    name = Column("name", String(255), nullable=False)
    created_at = Column("created_date_time", DateTime, default=datetime.now)