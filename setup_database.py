"""
Database setup script to populate initial fitness classes.
Run this script to add sample data to the database.
"""

from datetime import datetime, timedelta
import pytz
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models import FitnessClass

# Create tables
Base.metadata.create_all(bind=engine)

def create_sample_classes():
    """Create sample fitness classes for testing."""
    db = SessionLocal()
    
    try:
        # Define IST timezone
        ist = pytz.timezone('Asia/Kolkata')
        
        # Sample classes data
        sample_classes = [
            {
                "name": "Hatha Yoga",
                "instructor": "Priya Sharma",
                "class_datetime": datetime.now(ist) + timedelta(days=1, hours=9),
                "total_slots": 15,
                "description": "Gentle yoga focusing on basic postures and breathing techniques"
            },
            {
                "name": "Power Yoga",
                "instructor": "Rahul Kumar",
                "class_datetime": datetime.now(ist) + timedelta(days=1, hours=18),
                "total_slots": 12,
                "description": "Dynamic yoga flow for strength and flexibility"
            },
            {
                "name": "Zumba Dance Fitness",
                "instructor": "Maria Rodriguez",
                "class_datetime": datetime.now(ist) + timedelta(days=2, hours=19),
                "total_slots": 20,
                "description": "High-energy dance workout with Latin music"
            },
            {
                "name": "HIIT Training",
                "instructor": "Alex Johnson",
                "class_datetime": datetime.now(ist) + timedelta(days=3, hours=7),
                "total_slots": 10,
                "description": "High-intensity interval training for maximum calorie burn"
            },
            {
                "name": "Pilates Core",
                "instructor": "Sarah Thompson",
                "class_datetime": datetime.now(ist) + timedelta(days=3, hours=17),
                "total_slots": 12,
                "description": "Core strengthening and flexibility with Pilates techniques"
            },
            {
                "name": "Vinyasa Flow",
                "instructor": "Amit Patel",
                "class_datetime": datetime.now(ist) + timedelta(days=4, hours=8),
                "total_slots": 14,
                "description": "Flowing yoga sequences synchronized with breath"
            },
            {
                "name": "CrossFit WOD",
                "instructor": "Mike Wilson",
                "class_datetime": datetime.now(ist) + timedelta(days=5, hours=18),
                "total_slots": 8,
                "description": "Workout of the Day - functional fitness training"
            },
            {
                "name": "Meditation & Mindfulness",
                "instructor": "Dr. Anjali Gupta",
                "class_datetime": datetime.now(ist) + timedelta(days=6, hours=19),
                "total_slots": 25,
                "description": "Guided meditation and mindfulness practices"
            }
        ]
        
        # Check if classes already exist
        existing_classes = db.query(FitnessClass).count()
        if existing_classes > 0:
            print(f"Database already contains {existing_classes} classes. Skipping sample data creation.")
            return
        
        # Create classes
        for class_data in sample_classes:
            fitness_class = FitnessClass(
                name=class_data["name"],
                instructor=class_data["instructor"],
                class_datetime=class_data["class_datetime"],
                total_slots=class_data["total_slots"],
                available_slots=class_data["total_slots"],
                description=class_data["description"]
            )
            db.add(fitness_class)
        
        db.commit()
        print(f"Successfully created {len(sample_classes)} sample fitness classes!")
        
        # Display created classes
        print("\nCreated Classes:")
        print("-" * 80)
        for cls in db.query(FitnessClass).all():
            print(f"ID: {cls.id} | {cls.name} | {cls.instructor} | {cls.class_datetime} | Slots: {cls.available_slots}/{cls.total_slots}")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating sample classes: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Setting up database with sample data...")
    create_sample_classes()
    print("Database setup completed!")