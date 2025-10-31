# Hospital Management System - Backend API

FastAPI backend for the Hospital Management System with MySQL database.

## Features

- ✅ Patient Management (CRUD)
- ✅ Doctor Management (CRUD)
- ✅ Appointment Scheduling (CRUD)
- ✅ Prescription Management (CRUD)
- ✅ Dashboard Statistics
- ✅ RESTful API
- ✅ MySQL Database
- ✅ SQLAlchemy ORM
- ✅ Pydantic Validation
- ✅ CORS Enabled
- ✅ Auto-generated API Documentation

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **MySQL** - Database
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL Server
- pip

### Setup Steps

1. **Create Virtual Environment**
```bash
cd backend
python -m venv venv
```

2. **Activate Virtual Environment**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Database**

Create MySQL database:
```sql
CREATE DATABASE hospital_db;
```

5. **Create `.env` File**
```bash
# Copy the example
cp .env.example .env

# Edit .env with your database credentials
DATABASE_URL=mysql+pymysql://your_user:your_password@localhost:3306/hospital_db
```

6. **Run the Application**
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload --port 8000
```

7. **Seed Sample Data (Optional)**
```bash
python seed_data.py
```

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Patients
- `GET /api/patients` - Get all patients
- `GET /api/patients/{id}` - Get patient by ID
- `POST /api/patients` - Create patient
- `PUT /api/patients/{id}` - Update patient
- `DELETE /api/patients/{id}` - Delete patient

### Doctors
- `GET /api/doctors` - Get all doctors
- `GET /api/doctors/{id}` - Get doctor by ID
- `POST /api/doctors` - Create doctor
- `PUT /api/doctors/{id}` - Update doctor
- `DELETE /api/doctors/{id}` - Delete doctor

### Appointments
- `GET /api/appointments` - Get all appointments
- `GET /api/appointments/{id}` - Get appointment by ID
- `POST /api/appointments` - Create appointment
- `PUT /api/appointments/{id}` - Update appointment
- `DELETE /api/appointments/{id}` - Delete appointment

### Prescriptions
- `GET /api/prescriptions` - Get all prescriptions
- `GET /api/prescriptions/{id}` - Get prescription by ID
- `GET /api/prescriptions/patient/{patient_id}` - Get patient's prescriptions
- `POST /api/prescriptions` - Create prescription
- `PUT /api/prescriptions/{id}` - Update prescription
- `DELETE /api/prescriptions/{id}` - Delete prescription

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics

## Project Structure

```
backend/
├── main.py              # FastAPI application & routes
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas
├── crud.py              # Database operations
├── database.py          # Database configuration
├── config.py            # Application settings
├── seed_data.py         # Sample data seeder
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Configuration

Edit `.env` file:

```env
# Database
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/hospital_db

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS
FRONTEND_URL=http://localhost:3000
```

## Database Models

### Patient
- id (UUID)
- name
- age
- gender
- contact
- address
- medical_history
- created_at
- updated_at

### Doctor
- id (UUID)
- name
- specialization
- contact
- email
- created_at
- updated_at

### Appointment
- id (UUID)
- patient_id (FK)
- doctor_id (FK)
- date
- time
- reason
- status
- created_at
- updated_at

### Prescription
- id (UUID)
- patient_id (FK)
- doctor_id (FK)
- diagnosis
- medications
- instructions
- date
- attachments
- created_at
- updated_at

## Testing API

### Using Swagger UI
Visit http://localhost:8000/docs

### Using curl

Create a patient:
```bash
curl -X POST "http://localhost:8000/api/patients" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 35,
    "gender": "Male",
    "contact": "+1234567890",
    "address": "123 Main St",
    "medical_history": "None"
  }'
```

Get all patients:
```bash
curl http://localhost:8000/api/patients
```

## Error Handling

All errors return JSON:
```json
{
  "detail": "Error message"
}
```

Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## CORS

CORS is enabled for:
- http://localhost:3000 (Frontend)
- All methods and headers allowed

## Development

### Run in Development Mode
```bash
uvicorn main:app --reload --port 8000
```

### View Logs
All SQL queries are logged when DEBUG=True

### Database Migrations (Future)
Use Alembic for migrations:
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Troubleshooting

### Port Already in Use
Change port in `.env` or command:
```bash
uvicorn main:app --reload --port 8001
```

### Database Connection Error
- Check MySQL is running
- Verify credentials in `.env`
- Ensure database exists

### Module Not Found
```bash
pip install -r requirements.txt
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Use production database
3. Use gunicorn with uvicorn workers:
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Support

For issues or questions:
1. Check API documentation at /docs
2. Review error logs
3. Verify database connection
4. Test endpoints with Swagger UI

## License

MIT














