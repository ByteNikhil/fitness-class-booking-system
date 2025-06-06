"""
Utility functions for the Fitness Studio Booking API.
Handles timezone conversions and common helper functions.
"""

import pytz
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DEFAULT_TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

def get_timezone(timezone_str: str = None) -> pytz.timezone:
    """
    Get timezone object from string.
    
    Args:
        timezone_str: Timezone string (e.g., 'Asia/Kolkata')
        
    Returns:
        pytz.timezone object
    """
    tz_str = timezone_str or DEFAULT_TIMEZONE
    try:
        return pytz.timezone(tz_str)
    except pytz.exceptions.UnknownTimeZoneError:
        return pytz.timezone(DEFAULT_TIMEZONE)

def convert_datetime_to_timezone(dt: datetime, target_timezone: str = None) -> datetime:
    """
    Convert datetime to specified timezone.
    
    Args:
        dt: Datetime object to convert
        target_timezone: Target timezone string
        
    Returns:
        Converted datetime object
    """
    if dt.tzinfo is None:
        # Assume UTC if no timezone info
        dt = pytz.UTC.localize(dt)
    
    target_tz = get_timezone(target_timezone)
    return dt.astimezone(target_tz)

def format_datetime_for_response(dt: datetime, timezone_str: str = None) -> datetime:
    """
    Format datetime for API response with proper timezone.
    
    Args:
        dt: Datetime to format
        timezone_str: Target timezone
        
    Returns:
        Formatted datetime
    """
    return convert_datetime_to_timezone(dt, timezone_str)

def validate_future_datetime(dt: datetime) -> bool:
    """
    Validate that datetime is in the future.
    
    Args:
        dt: Datetime to validate
        
    Returns:
        True if datetime is in future, False otherwise
    """
    now = datetime.utcnow()
    if dt.tzinfo is None:
        dt = pytz.UTC.localize(dt)
    now = pytz.UTC.localize(now)
    
    return dt > now