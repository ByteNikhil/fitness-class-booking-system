"""
Unit tests for the main FastAPI application endpoints.
Tests API functionality, error handling, and data validation.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import pytz

from app.main import app
from app.database import get_db, Base
from app.models import FitnessClass

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    """Setup test database with sample data."""
    Base.metadata.create_all(bind=engine)
    
    # Add sample class
    db = TestingSessionLocal()
    ist = pytz.timezone('Asia/Kolkata')
    
    sample_class = FitnessClass(
        name="Test Yoga",
        instructor="Test Instructor",
        class_datetime=datetime.now(ist) + timedelta(days=1),
        total_slots=5,
        available_slots=5,
        description="Test class"
    )
    db.add(sample_class)
    db.commit()
    db.close()
    
    yield
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)

def test_read_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_get_classes(setup_database):
    """Test retrieving fitness classes."""
    response = client.get("/classes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Check class structure
    if data:
        class_data = data[0]
        required_fields = ["id", "name", "instructor", "class_datetime", "total_slots", "available_slots"]
        for field in required_fields:
            assert field in class_data