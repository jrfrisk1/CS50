from sqlalchemy import Column, Integer, String, Date, Time, Text, Enum, DateTime, create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

url = "sqlite:///events.db"  # Change this to a file-based database if needed

# Create an engine for a SQLite database
engine = create_engine(url, echo=True)

Base = declarative_base()


class Event(Base):
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
    





def init_db():
    """Create all tables in the database"""
    Base.metadata.create_all(engine)
