from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date, time
from typing import Optional, List, Any
from enum import Enum


# Enums
class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    STAFF = "staff"


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRoleEnum = UserRoleEnum.STAFF


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User


class TokenData(BaseModel):
    user_id: Optional[str] = None


class AppointmentStatusEnum(str, Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    RESCHEDULED = "Rescheduled"


# Patient Schemas
class PatientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    age: int = Field(..., gt=0, lt=150)
    gender: GenderEnum
    contact: str = Field(..., min_length=1, max_length=20)
    address: str = Field(..., min_length=1)
    medical_history: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    age: Optional[int] = Field(None, gt=0, lt=150)
    gender: Optional[GenderEnum] = None
    contact: Optional[str] = Field(None, min_length=1, max_length=20)
    address: Optional[str] = Field(None, min_length=1)
    medical_history: Optional[str] = None


class Patient(PatientBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Doctor Schemas
class DoctorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    specialization: str = Field(..., min_length=1, max_length=100)
    contact: str = Field(..., min_length=1, max_length=20)
    email: EmailStr


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    specialization: Optional[str] = Field(None, min_length=1, max_length=100)
    contact: Optional[str] = Field(None, min_length=1, max_length=20)
    email: Optional[EmailStr] = None


class Doctor(DoctorBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Appointment Schemas
class AppointmentBase(BaseModel):
    patient_id: str
    doctor_id: str
    date: date
    time: time
    reason: str = Field(..., min_length=1)
    status: AppointmentStatusEnum = AppointmentStatusEnum.SCHEDULED


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    patient_id: Optional[str] = None
    doctor_id: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time] = None
    reason: Optional[str] = Field(None, min_length=1)
    status: Optional[AppointmentStatusEnum] = None


class Appointment(AppointmentBase):
    id: str
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Prescription Schemas
class PrescriptionBase(BaseModel):
    patient_id: str
    doctor_id: str
    diagnosis: str = Field(..., min_length=1)
    medications: str = Field(..., min_length=1)
    instructions: Optional[str] = None
    date: date
    attachments: Optional[List[str]] = None


class PrescriptionCreate(PrescriptionBase):
    pass


class PrescriptionUpdate(BaseModel):
    patient_id: Optional[str] = None
    doctor_id: Optional[str] = None
    diagnosis: Optional[str] = Field(None, min_length=1)
    medications: Optional[str] = Field(None, min_length=1)
    instructions: Optional[str] = None
    date: Optional[date] = None
    attachments: Optional[List[str]] = None


class Prescription(PrescriptionBase):
    id: str
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Dashboard Schema
class DashboardStats(BaseModel):
    total_patients: int
    total_appointments: int
    active_prescriptions: int
    today_appointments: int


# API Response Schema
class ApiResponse(BaseModel):
    data: Any
    message: Optional[str] = None
    success: bool = True

