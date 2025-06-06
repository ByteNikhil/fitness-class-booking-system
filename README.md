# Fitness Class Booking System

A comprehensive RESTful API for managing fitness class bookings at a studio. Built with FastAPI, SQLAlchemy, and SQLite for optimal performance and ease of deployment.

## 🚀 Features

- **Class Management**: View all upcoming fitness classes with detailed information
- **Booking System**: Book classes with real-time availability checking
- **Client Management**: Retrieve booking history by email address
- **Timezone Support**: Dynamic timezone conversion for class schedules
- **Data Validation**: Comprehensive input validation and error handling
- **Duplicate Prevention**: Prevents duplicate bookings for the same class
- **Logging**: Detailed logging for debugging and monitoring
- **API Documentation**: Auto-generated interactive API documentation

## 🏗️ Project Structure

```
fitness-class-booking-system/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application and routes
│   ├── models.py            # SQLAlchemy database models
│   ├── database.py          # Database configuration
│   ├── schemas.py           # Pydantic models for validation
│   ├── crud.py              # Database operations
│   └── utils.py             # Utility functions and helpers
├── tests/
│   ├── __init__.py          # Test package initialization
│   ├── test_main.py         # API endpoint tests
│   └── test_crud.py         # Database operation tests
├── requirements.txt         # Python dependencies
├── setup_database.py       # Database setup with sample data
├── .env                     # Environment variables
└── README.md               # Project documentation
```

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.104.1
- **Database**: SQLite with SQLAlchemy ORM
- **Validation**: Pydantic models
- **Authentication**: Basic email validation
- **Testing**: Pytest with HTTP client testing
- **Timezone**: Pytz for timezone management
- **Documentation**: Auto-generated OpenAPI/Swagger docs

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fitness-class-booking-system.git
cd fitness-studio-booking-api
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///./fitness_studio.db
TIMEZONE=Asia/Kolkata
```

### 5. Initialize Database

```bash
python setup_database.py
```

This will create the SQLite database and populate it with sample fitness classes.

### 6. Run the Application

```bash
# Development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## 📖 API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### 1. Get All Classes
```http
GET /classes?timezone=America/New_York
```

**Description**: Retrieve all upcoming fitness classes with availability information.

**Query Parameters**:
- `timezone` (optional): Target timezone for class times (e.g., 'America/New_York', 'Europe/London')

**Response**:
```json
[
  {
    "id": 1,
    "name": "Hatha Yoga",
    "instructor": "Priya Sharma",
    "class_datetime": "2025-06-07T09:00:00+05:30",
    "total_slots": 15,
    "available_slots": 12,
    "description": "Gentle yoga focusing on basic postures and breathing techniques",
    "created_at": "2025-06-06T10:30:00"
  }
]
```

#### 2. Book a Class
```http
POST /book
```

**Description**: Book a spot in a fitness class.

**Request Body**:
```json
{
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john.doe@example.com"
}
```

**Response**:
```json
{
  "id": 1,
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john.doe@example.com",
  "booking_datetime": "2025-06-06T15:30:00",
  "status": "confirmed",
  "fitness_class": {
    "id": 1,
    "name": "Hatha Yoga",
    "instructor": "Priya Sharma",
    "class_datetime": "2025-06-07T09:00:00+05:30",
    "total_slots": 15,
    "available_slots": 11,
    "description": "Gentle yoga focusing on basic postures and breathing techniques"
  }
}
```

#### 3. Get Bookings by Email
```http
GET /bookings?email=john.doe@example.com
```

**Description**: Retrieve all bookings for a specific email address.

**Query Parameters**:
- `email` (required): Client's email address

**Response**:
```json
{
  "bookings": [
    {
      "id": 1,
      "class_id": 1,
      "client_name": "John Doe",
      "client_email": "john.doe@example.com",
      "booking_datetime": "2025-06-06T15:30:00",
      "status": "confirmed",
      "fitness_class": {
        "id": 1,
        "name": "Hatha Yoga",
        "instructor": "Priya Sharma",
        "class_datetime": "2025-06-07T09:00:00+05:30",
        "total_slots": 15,
        "available_slots": 11
      }
    }
  ],
  "total_count": 1
}
```

#### 4. Additional Endpoints
```http
GET /                    # API information
GET /health             # Health check
```

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test Files
```bash
pytest tests/test_main.py -v
pytest tests/test_crud.py -v
```

### Test Coverage
```bash
pytest --cov=app tests/
```

## 📝 Sample API Requests

### Using cURL

#### Get All Classes
```bash
curl -X GET "http://localhost:8000/classes" \
  -H "accept: application/json"
```

#### Book a Class
```bash
curl -X POST "http://localhost:8000/book" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "client_name": "John Doe",
    "client_email": "john.doe@example.com"
  }'
```

#### Get Bookings
```bash
curl -X GET "http://localhost:8000/bookings?email=john.doe@example.com" \
  -H "accept: application/json"
```

### Using Postman

1. **Import Collection**: Create a new Postman collection
2. **Set Base URL**: `http://localhost:8000`
3. **Add Requests**: Use the sample requests above
4. **Environment Variables**: Set up variables for base URL and test data

## 🌍 Timezone Management

The API supports dynamic timezone conversion for class schedules:

- **Default Timezone**: Asia/Kolkata (IST)
- **Supported Timezones**: All pytz-supported timezones
- **Usage**: Add `?timezone=America/New_York` to `/classes` endpoint
- **Error Handling**: Falls back to default timezone for invalid timezone strings

### Example Timezone Conversions
```bash
# Get classes in New York time
curl "http://localhost:8000/classes?timezone=America/New_York"

# Get classes in London time
curl "http://localhost:8000/classes?timezone=Europe/London"

# Get classes in Tokyo time
curl "http://localhost:8000/classes?timezone=Asia/Tokyo"
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLite database file path | `sqlite:///./fitness_studio.db` |
| `TIMEZONE` | Default timezone for the application | `Asia/Kolkata` |

### Database Schema

#### FitnessClass Table
- `id`: Primary key
- `name`: Class name (e.g., "Hatha Yoga")
- `instructor`: Instructor name
- `class_datetime`: Class date and time
- `total_slots`: Total available slots
- `available_slots`: Currently available slots
- `description`: Class description
- `created_at`: Record creation timestamp

#### Booking Table
- `id`: Primary key
- `class_id`: Foreign key to FitnessClass
- `client_name`: Client's full name
- `client_email`: Client's email address
- `booking_datetime`: Booking creation timestamp
- `status`: Booking status (default: "confirmed")

## 🚨 Error Handling

The API implements comprehensive error handling:

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request (validation errors)
- `404`: Not Found
- `500`: Internal Server Error

### Common Error Responses

#### Validation Error
```json
{
  "detail": "Client name must be at least 2 characters long"
}
```

#### Booking Error
```json
{
  "detail": "No available slots for this class"
}
```

#### Not Found Error
```json
{
  "detail": "Class not found"
}
```

## 📊 Sample Data

The application comes with pre-populated sample data including:

- **8 Different Classes**: Yoga, Zumba, HIIT, Pilates, etc.
- **Various Instructors**: Diverse instructor profiles
- **Different Time Slots**: Morning, evening, and weekend classes
- **Varying Capacities**: Classes with 8-25 slots
- **Realistic Scheduling**: Classes spread across the next week

## 🔒 Security Considerations

- **Input Validation**: All inputs are validated using Pydantic models
- **SQL Injection Prevention**: SQLAlchemy ORM provides protection
- **Email Validation**: Email format validation for client emails
- **Error Handling**: Detailed error messages without exposing sensitive information
- **Logging**: Comprehensive logging for security monitoring

## 🚀 Deployment

### Local Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- SQLAlchemy for robust ORM capabilities
- Pydantic for data validation
- The Python community for amazing tools and libraries

---

**Happy Coding! 🎉**
