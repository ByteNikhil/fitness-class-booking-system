"""
SQLAlchemy models for the Fitness Studio Booking API.
Defines the database schema for classes and bookings.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class FitnessClass(Base):
    """
    Model representing a fitness class in the studio.
    Stores class information including schedule, instructor, and capacity.
    """
    __tablename__ = "fitness_classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    instructor = Column(String(100), nullable=False)
    class_datetime = Column(DateTime, nullable=False, index=True)
    total_slots = Column(Integer, nullable=False)
    available_slots = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with bookings
    bookings = relationship("Booking", back_populates="fitness_class")
    
    def __repr__(self):
        return f"<FitnessClass(name='{self.name}', instructor='{self.instructor}')>"

class Booking(Base):
    """
    Model representing a booking made by a client for a fitness class.
    Stores booking details and client information.
    """
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("fitness_classes.id"), nullable=False)
    client_name = Column(String(100), nullable=False)
    client_email = Column(String(255), nullable=False, index=True)
    booking_datetime = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="confirmed")
    
    # Relationship with fitness class
    fitness_class = relationship("FitnessClass", back_populates="bookings")
    
    def __repr__(self):
        return f"<Booking(client_name='{self.client_name}', class_id={self.class_id})>"