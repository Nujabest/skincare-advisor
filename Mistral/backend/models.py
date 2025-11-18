from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

from backend.db import Base


class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    result = Column(JSON)
    date = Column(DateTime, default=datetime.utcnow)
