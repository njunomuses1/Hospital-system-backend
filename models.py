from sqlalchemy import Column, String, Integer, Text, DateTime, Enum, ForeignKey, Date, Time, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum('admin', 'doctor', 'staff'), default='staff', nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False, index=True)
    age = Column(Integer, nullable=False)
    gender = Column(Enum('Male', 'Female', 'Other'), nullable=False)
    contact = Column(String(20), nullable=False)
    address = Column(Text, nullable=False)
    medical_history = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    prescriptions = relationship("Prescription", back_populates="patient", cascade="all, delete-orphan")


class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False, index=True)
    specialization = Column(String(100), nullable=False)
    contact = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")
    prescriptions = relationship("Prescription", back_populates="doctor", cascade="all, delete-orphan")


class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    patient_id = Column(String(36), ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    doctor_id = Column(String(36), ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(
        Enum('Scheduled', 'Completed', 'Cancelled', 'Rescheduled'),
        default='Scheduled',
        nullable=False,
        index=True
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")


class Prescription(Base):
    __tablename__ = "prescriptions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    patient_id = Column(String(36), ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    doctor_id = Column(String(36), ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False)
    diagnosis = Column(Text, nullable=False)
    medications = Column(Text, nullable=False)
    instructions = Column(Text, nullable=True)
    date = Column(Date, nullable=False, index=True)
    attachments = Column(Text, nullable=True)  # JSON string or comma-separated file paths
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")

