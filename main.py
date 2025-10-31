from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from database import get_db, init_db
from config import settings
import models
import schemas
import crud
import auth
import routes_auth


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Hospital Management System API",
)

# Configure CORS - Allow development and production environments
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Include routers
app.include_router(routes_auth.router)


# Initialize database on startup
@app.on_event("startup")
def on_startup():
    try:
        init_db()
        print(f"✅ Database initialized")
    except Exception as e:
        error_msg = str(e)
        print(f"⚠️  Database initialization failed: {type(e).__name__}")
        if "Access denied" in error_msg:
            print(f"\n💡 MySQL Connection Error!")
            print(f"   The backend will start, but login/registration won't work until MySQL is configured.")
            print(f"\n   To fix:")
            print(f"   1. Verify MySQL root password in backend/.env")
            print(f"   2. Run: connect-mysql.bat (to create database)")
            print(f"   3. Or manually: CREATE DATABASE hospital_db;")
        else:
            print(f"   Error: {error_msg}")
    
    print(f"✅ {settings.APP_NAME} v{settings.VERSION} is running")
    print(f"✅ Environment: {settings.ENVIRONMENT}")
    print(f"✅ API available at: http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"✅ Authentication enabled with JWT")
    print(f"✅ CORS Origins: {', '.join(settings.get_cors_origins()[:3])}...")


# Root endpoint
@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Health check endpoint for Railway
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


# ========== PATIENT ENDPOINTS ==========
@app.get("/api/patients", response_model=schemas.ApiResponse)
def get_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get all patients (Protected route)"""
    try:
        patients = crud.get_patients(db, skip=skip, limit=limit)
        return schemas.ApiResponse(data=patients, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/patients/{patient_id}", response_model=schemas.ApiResponse)
def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get a specific patient by ID (Protected route)"""
    patient = crud.get_patient(db, patient_id=patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return schemas.ApiResponse(data=patient, success=True)


@app.post("/api/patients", response_model=schemas.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Create a new patient (Protected route)"""
    try:
        db_patient = crud.create_patient(db=db, patient=patient)
        return schemas.ApiResponse(
            data=db_patient,
            message="Patient created successfully",
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/patients/{patient_id}", response_model=schemas.ApiResponse)
def update_patient(
    patient_id: str,
    patient: schemas.PatientUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Update a patient (Protected route)"""
    db_patient = crud.update_patient(db=db, patient_id=patient_id, patient=patient)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return schemas.ApiResponse(
        data=db_patient,
        message="Patient updated successfully",
        success=True
    )


@app.delete("/api/patients/{patient_id}", response_model=schemas.ApiResponse)
def delete_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Delete a patient (Protected route)"""
    success = crud.delete_patient(db=db, patient_id=patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return schemas.ApiResponse(
        data=None,
        message="Patient deleted successfully",
        success=True
    )


# ========== DOCTOR ENDPOINTS ==========
@app.get("/api/doctors", response_model=schemas.ApiResponse)
def get_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all doctors"""
    try:
        doctors = crud.get_doctors(db, skip=skip, limit=limit)
        return schemas.ApiResponse(data=doctors, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/doctors/{doctor_id}", response_model=schemas.ApiResponse)
def get_doctor(doctor_id: str, db: Session = Depends(get_db)):
    """Get a specific doctor by ID"""
    doctor = crud.get_doctor(db, doctor_id=doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return schemas.ApiResponse(data=doctor, success=True)


@app.post("/api/doctors", response_model=schemas.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    """Create a new doctor"""
    try:
        db_doctor = crud.create_doctor(db=db, doctor=doctor)
        return schemas.ApiResponse(
            data=db_doctor,
            message="Doctor created successfully",
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/doctors/{doctor_id}", response_model=schemas.ApiResponse)
def update_doctor(doctor_id: str, doctor: schemas.DoctorUpdate, db: Session = Depends(get_db)):
    """Update a doctor"""
    db_doctor = crud.update_doctor(db=db, doctor_id=doctor_id, doctor=doctor)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return schemas.ApiResponse(
        data=db_doctor,
        message="Doctor updated successfully",
        success=True
    )


@app.delete("/api/doctors/{doctor_id}", response_model=schemas.ApiResponse)
def delete_doctor(doctor_id: str, db: Session = Depends(get_db)):
    """Delete a doctor"""
    success = crud.delete_doctor(db=db, doctor_id=doctor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return schemas.ApiResponse(
        data=None,
        message="Doctor deleted successfully",
        success=True
    )


# ========== APPOINTMENT ENDPOINTS ==========
@app.get("/api/appointments", response_model=schemas.ApiResponse)
def get_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all appointments"""
    try:
        appointments = crud.get_appointments(db, skip=skip, limit=limit)
        return schemas.ApiResponse(data=appointments, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/appointments/{appointment_id}", response_model=schemas.ApiResponse)
def get_appointment(appointment_id: str, db: Session = Depends(get_db)):
    """Get a specific appointment by ID"""
    appointment = crud.get_appointment(db, appointment_id=appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return schemas.ApiResponse(data=appointment, success=True)


@app.post("/api/appointments", response_model=schemas.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    """Create a new appointment"""
    try:
        # Verify patient exists
        patient = crud.get_patient(db, appointment.patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Verify doctor exists
        doctor = crud.get_doctor(db, appointment.doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        
        db_appointment = crud.create_appointment(db=db, appointment=appointment)
        return schemas.ApiResponse(
            data=db_appointment,
            message="Appointment created successfully",
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/appointments/{appointment_id}", response_model=schemas.ApiResponse)
def update_appointment(appointment_id: str, appointment: schemas.AppointmentUpdate, db: Session = Depends(get_db)):
    """Update an appointment"""
    try:
        # Verify patient exists if provided
        if appointment.patient_id:
            patient = crud.get_patient(db, appointment.patient_id)
            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found")
        
        # Verify doctor exists if provided
        if appointment.doctor_id:
            doctor = crud.get_doctor(db, appointment.doctor_id)
            if not doctor:
                raise HTTPException(status_code=404, detail="Doctor not found")
        
        db_appointment = crud.update_appointment(db=db, appointment_id=appointment_id, appointment=appointment)
        if db_appointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return schemas.ApiResponse(
            data=db_appointment,
            message="Appointment updated successfully",
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/appointments/{appointment_id}", response_model=schemas.ApiResponse)
def delete_appointment(appointment_id: str, db: Session = Depends(get_db)):
    """Delete an appointment"""
    success = crud.delete_appointment(db=db, appointment_id=appointment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return schemas.ApiResponse(
        data=None,
        message="Appointment deleted successfully",
        success=True
    )


# ========== PRESCRIPTION ENDPOINTS ==========
@app.get("/api/prescriptions", response_model=schemas.ApiResponse)
def get_prescriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all prescriptions"""
    try:
        prescriptions = crud.get_prescriptions(db, skip=skip, limit=limit)
        return schemas.ApiResponse(data=prescriptions, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/prescriptions/{prescription_id}", response_model=schemas.ApiResponse)
def get_prescription(prescription_id: str, db: Session = Depends(get_db)):
    """Get a specific prescription by ID"""
    prescription = crud.get_prescription(db, prescription_id=prescription_id)
    if prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return schemas.ApiResponse(data=prescription, success=True)


@app.get("/api/prescriptions/patient/{patient_id}", response_model=schemas.ApiResponse)
def get_prescriptions_by_patient(patient_id: str, db: Session = Depends(get_db)):
    """Get all prescriptions for a specific patient"""
    try:
        prescriptions = crud.get_prescriptions_by_patient(db, patient_id=patient_id)
        return schemas.ApiResponse(data=prescriptions, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/prescriptions", response_model=schemas.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_prescription(prescription: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    """Create a new prescription"""
    try:
        # Verify patient exists
        patient = crud.get_patient(db, prescription.patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Verify doctor exists
        doctor = crud.get_doctor(db, prescription.doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        
        db_prescription = crud.create_prescription(db=db, prescription=prescription)
        return schemas.ApiResponse(
            data=db_prescription,
            message="Prescription created successfully",
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/prescriptions/{prescription_id}", response_model=schemas.ApiResponse)
def update_prescription(prescription_id: str, prescription: schemas.PrescriptionUpdate, db: Session = Depends(get_db)):
    """Update a prescription"""
    try:
        # Verify patient exists if provided
        if prescription.patient_id:
            patient = crud.get_patient(db, prescription.patient_id)
            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found")
        
        # Verify doctor exists if provided
        if prescription.doctor_id:
            doctor = crud.get_doctor(db, prescription.doctor_id)
            if not doctor:
                raise HTTPException(status_code=404, detail="Doctor not found")
        
        db_prescription = crud.update_prescription(db=db, prescription_id=prescription_id, prescription=prescription)
        if db_prescription is None:
            raise HTTPException(status_code=404, detail="Prescription not found")
        return schemas.ApiResponse(
            data=db_prescription,
            message="Prescription updated successfully",
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/prescriptions/{prescription_id}", response_model=schemas.ApiResponse)
def delete_prescription(prescription_id: str, db: Session = Depends(get_db)):
    """Delete a prescription"""
    success = crud.delete_prescription(db=db, prescription_id=prescription_id)
    if not success:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return schemas.ApiResponse(
        data=None,
        message="Prescription deleted successfully",
        success=True
    )


# ========== DASHBOARD ENDPOINT ==========
@app.get("/api/dashboard/stats", response_model=schemas.ApiResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    try:
        stats = crud.get_dashboard_stats(db)
        return schemas.ApiResponse(data=stats, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )

