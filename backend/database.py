from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./cards.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Card(Base):
    __tablename__ = "cards"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    barcode = Column(String)
    image = Column(String)
