"""
CRUD operations for the Fitness Studio Booking API.
Handles database operations for classes and bookings.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List, Optional
import logging

from app.models import FitnessClass, Booking
from app.schemas import FitnessClassCreate, BookingRequest
from app.utils import validate_future_datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_upcoming_classes(db: Session, timezone_str: str = None) -> List[FitnessClass]:
    """
    Retrieve all upcoming fitness classes.
    
    Args:
        db: Database session
        timezone_str: Timezone for filtering
        
    Returns:
        List of upcoming fitness classes
    """
    try:
        current_time = datetime.utcnow()
        classes = db.query(FitnessClass).filter(
            FitnessClass.class_datetime > current_time,
            FitnessClass.available_slots > 0
        ).order_by(FitnessClass.class_datetime).all()
        
        logger.info(f"Retrieved {len(classes)} upcoming classes")
        return classes
    except Exception as e:
        logger.error(f"Error retrieving upcoming classes: {str(e)}")
        raise

def get_class_by_id(db: Session, class_id: int) -> Optional[FitnessClass]:
    """
    Retrieve a fitness class by ID.
    
    Args:
        db: Database session
        class_id: ID of the class to retrieve
        
    Returns:
        FitnessClass object or None if not found
    """
    try:
        fitness_class = db.query(FitnessClass).filter(FitnessClass.id == class_id).first()
        if fitness_class:
            logger.info(f"Retrieved class with ID {class_id}")
        else:
            logger.warning(f"Class with ID {class_id} not found")
        return fitness_class
    except Exception as e:
        logger.error(f"Error retrieving class {class_id}: {str(e)}")
        raise

def create_booking(db: Session, booking_request: BookingRequest) -> Booking:
    """
    Create a new booking for a fitness class.
    
    Args:
        db: Database session
        booking_request: Booking request data
        
    Returns:
        Created booking object
        
    Raises:
        ValueError: If class not found, no slots available, or class is in the past
    """
    try:
        # Get the fitness class
        fitness_class = get_class_by_id(db, booking_request.class_id)
        if not fitness_class:
            logger.warning(f"Booking attempt for non-existent class {booking_request.class_id}")
            raise ValueError("Class not found")
        
        # Check if class is in the future
        if not validate_future_datetime(fitness_class.class_datetime):
            logger.warning(f"Booking attempt for past class {booking_request.class_id}")
            raise ValueError("Cannot book classes in the past")
        
        # Check if slots are available
        if fitness_class.available_slots <= 0:
            logger.warning(f"Booking attempt for fully booked class {booking_request.class_id}")
            raise ValueError("No available slots for this class")
        
        # Check for duplicate booking
        existing_booking = db.query(Booking).filter(
            and_(
                Booking.class_id == booking_request.class_id,
                Booking.client_email == booking_request.client_email
            )
        ).first()
        
        if existing_booking:
            logger.warning(f"Duplicate booking attempt for {booking_request.client_email}")
            raise ValueError("You have already booked this class")
        
        # Create the booking
        new_booking = Booking(
            class_id=booking_request.class_id,
            client_name=booking_request.client_name,
            client_email=booking_request.client_email,
            booking_datetime=datetime.utcnow()
        )
        
        # Reduce available slots
        fitness_class.available_slots -= 1
        
        # Save to database
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        
        logger.info(f"Created booking {new_booking.id} for {booking_request.client_email}")
        return new_booking
        
    except ValueError:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating booking: {str(e)}")
        raise ValueError("Failed to create booking")

def get_bookings_by_email(db: Session, client_email: str) -> List[Booking]:
    """
    Retrieve all bookings for a specific email address.
    
    Args:
        db: Database session
        client_email: Client's email address
        
    Returns:
        List of bookings for the specified email
    """
    try:
        bookings = db.query(Booking).filter(
            Booking.client_email == client_email
        ).order_by(Booking.booking_datetime.desc()).all()
        
        logger.info(f"Retrieved {len(bookings)} bookings for {client_email}")
        return bookings
    except Exception as e:
        logger.error(f"Error retrieving bookings for {client_email}: {str(e)}")
        raise

def create_fitness_class(db: Session, class_data: FitnessClassCreate) -> FitnessClass:
    """
    Create a new fitness class.
    
    Args:
        db: Database session
        class_data: Class creation data
        
    Returns:
        Created fitness class object
    """
    try:
        new_class = FitnessClass(
            name=class_data.name,
            instructor=class_data.instructor,
            class_datetime=class_data.class_datetime,
            total_slots=class_data.total_slots,
            available_slots=class_data.total_slots,
            description=class_data.description
        )
        
        db.add(new_class)
        db.commit()
        db.refresh(new_class)
        
        logger.info(f"Created fitness class {new_class.id}: {new_class.name}")
        return new_class
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating fitness class: {str(e)}")
        raise