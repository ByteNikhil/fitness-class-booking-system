"""
Pydantic schemas for request/response validation and serialization.
Defines the API contract for the Fitness Studio Booking API.
"""

from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import List, Optional

class FitnessClassBase(BaseModel):
    """Base schema for fitness class data."""
    name: str
    instructor: str
    class_datetime: datetime
    total_slots: int
    description: Optional[str] = None

class FitnessClassCreate(FitnessClassBase):
    """Schema for creating a new fitness class."""
    pass

class FitnessClassResponse(FitnessClassBase):
    """Schema for fitness class response with additional computed fields."""
    id: int
    available_slots: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class BookingRequest(BaseModel):
    """Schema for booking request validation."""
    class_id: int
    client_name: str
    client_email: EmailStr
    
    @validator('client_name')
    def validate_client_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Client name must be at least 2 characters long')
        return v.strip()

class BookingResponse(BaseModel):
    """Schema for booking response."""
    id: int
    class_id: int
    client_name: str
    client_email: str
    booking_datetime: datetime
    status: str
    fitness_class: FitnessClassResponse
    
    class Config:
        from_attributes = True

class BookingListResponse(BaseModel):
    """Schema for list of bookings response."""
    bookings: List[BookingResponse]
    total_count: int

class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None