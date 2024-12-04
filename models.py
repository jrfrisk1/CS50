from sqlalchemy import Column, Integer, String, Date, Time, Text, Enum, DateTime, create_engine, LargeBinary
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
import os

# Try to connect to Heroku Database if not make Sqlite Datbase
url = os.getenv("DATABASE_URL")  
if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)
else:
    url = "sqlite:///events.db"

 
# Create an engine for a given database
engine = create_engine(url, echo=True)
Base = declarative_base()


class Event(Base):
    """Class for Events"""
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    description = Column(Text)
    event_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    frequency = Column(String)
    status = Column(Enum('Pending', 'Approved', 'Denied', name='event_status'), default='Pending')  # Enum for status
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    host_link = Column(String)
    
    
    





def init_db():
    """Create all tables in the database"""
    Base.metadata.create_all(engine)
