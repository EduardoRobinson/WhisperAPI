from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Transcricoes(Base):
    __tablename__ = "transcricoes"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=True)