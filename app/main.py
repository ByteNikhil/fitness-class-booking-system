"""
Main FastAPI application for the Fitness Studio Booking API.
Defines API endpoints and handles HTTP requests/responses.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime

from app.database import get_db, engine, Base
from app.models import FitnessClass, Booking
from app.schemas import (
    FitnessClassResponse, BookingRequest, BookingResponse, 
    BookingListResponse, ErrorResponse
)
from app.crud import (
    get_upcoming_classes, create_booking, get_bookings_by_email,
    get_class_by_id
)
from app.utils import format_datetime_for_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Fitness Studio Booking API",
    description="A comprehensive API for managing fitness class bookings",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
async def read_root():
    """Root endpoint providing API information."""
    return {
        "message": "Welcome to Fitness Studio Booking API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "fitness-booking-api"
    }

@app.get("/classes", response_model=List[FitnessClassResponse])
async def get_classes(
    timezone: Optional[str] = Query(None, description="Timezone for class times (e.g., 'America/New_York')"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all upcoming fitness classes.
    
    Returns a list of available fitness classes with their details including:
    - Class name and instructor
    - Date and time (adjusted for specified timezone)
    - Available slots
    
    Args:
        timezone: Optional timezone for datetime conversion
        db: Database session dependency
        
    Returns:
        List of upcoming fitness classes
    """
    try:
        logger.info(f"Fetching upcoming classes with timezone: {timezone}")
        classes = get_upcoming_classes(db, timezone)
        
        # Format response with timezone conversion if specified
        response_classes = []
        for cls in classes:
            class_dict = {
                "id": cls.id,
                "name": cls.name,
                "instructor": cls.instructor,
                "class_datetime": format_datetime_for_response(cls.class_datetime, timezone),
                "total_slots": cls.total_slots,
                "available_slots": cls.available_slots,
                "description": cls.description,
                "created_at": cls.created_at
            }
            response_classes.append(FitnessClassResponse(**class_dict))
        
        logger.info(f"Successfully retrieved {len(response_classes)} classes")
        return response_classes
    
    except Exception as e:
        logger.error(f"Error fetching classes: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve classes"
        )

@app.post("/book", response_model=BookingResponse)
async def book_class(
    booking_request: BookingRequest,
    db: Session = Depends(get_db)
):
    """
    Book a spot in a fitness class.
    
    Creates a new booking for the specified class and client.
    Validates availability and prevents overbooking.
    
    Args:
        booking_request: Booking details including class_id, client_name, and client_email
        db: Database session dependency
        
    Returns:
        Created booking details
        
    Raises:
        HTTPException: If booking fails due to validation errors or unavailability
    """
    try:
        logger.info(f"Processing booking request for class {booking_request.class_id} by {booking_request.client_email}")
        
        # Create the booking
        new_booking = create_booking(db, booking_request)
        
        # Fetch the complete booking with class details for response
        booking_with_class = db.query(Booking).filter(Booking.id == new_booking.id).first()
        
        logger.info(f"Successfully created booking {new_booking.id}")
        return BookingResponse(
            id=booking_with_class.id,
            class_id=booking_with_class.class_id,
            client_name=booking_with_class.client_name,
            client_email=booking_with_class.client_email,
            booking_datetime=booking_with_class.booking_datetime,
            status=booking_with_class.status,
            fitness_class=FitnessClassResponse(
                id=booking_with_class.fitness_class.id,
                name=booking_with_class.fitness_class.name,
                instructor=booking_with_class.fitness_class.instructor,
                class_datetime=booking_with_class.fitness_class.class_datetime,
                total_slots=booking_with_class.fitness_class.total_slots,
                available_slots=booking_with_class.fitness_class.available_slots,
                description=booking_with_class.fitness_class.description,
                created_at=booking_with_class.fitness_class.created_at
            )
        )
    
    except ValueError as e:
        logger.warning(f"Booking validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing booking: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process booking"
        )

@app.get("/bookings", response_model=BookingListResponse)
async def get_bookings(
    email: str = Query(..., description="Client email address to retrieve bookings for"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all bookings for a specific email address.
    
    Returns comprehensive booking history including class details.
    
    Args:
        email: Client email address
        db: Database session dependency
        
    Returns:
        List of bookings with class details and total count
    """
    try:
        logger.info(f"Fetching bookings for email: {email}")
        
        # Validate email format
        if not email or "@" not in email:
            raise HTTPException(status_code=400, detail="Valid email address is required")
        
        bookings = get_bookings_by_email(db, email)
        
        # Format response with complete booking and class details
        booking_responses = []
        for booking in bookings:
            booking_response = BookingResponse(
                id=booking.id,
                class_id=booking.class_id,
                client_name=booking.client_name,
                client_email=booking.client_email,
                booking_datetime=booking.booking_datetime,
                status=booking.status,
                fitness_class=FitnessClassResponse(
                    id=booking.fitness_class.id,
                    name=booking.fitness_class.name,
                    instructor=booking.fitness_class.instructor,
                    class_datetime=booking.fitness_class.class_datetime,
                    total_slots=booking.fitness_class.total_slots,
                    available_slots=booking.fitness_class.available_slots,
                    description=booking.fitness_class.description,
                    created_at=booking.fitness_class.created_at
                )
            )
            booking_responses.append(booking_response)
        
        logger.info(f"Successfully retrieved {len(booking_responses)} bookings for {email}")
        return BookingListResponse(
            bookings=booking_responses,
            total_count=len(booking_responses)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching bookings for {email}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve bookings"
        )

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors with custom response."""
    return HTTPException(
        status_code=404,
        detail="The requested resource was not found"
    )

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """Handle 500 errors with custom response."""
    logger.error(f"Internal server error: {str(exc)}")
    return HTTPException(
        status_code=500,
        detail="Internal server error occurred"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)