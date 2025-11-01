from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import date
from typing import List, Optional
import models
import schemas


# ========== PATIENT CRUD ==========
def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[models.Patient]:
    return db.query(models.Patient).offset(skip).limit(limit).all()


def get_patient(db: Session, patient_id: str) -> Optional[models.Patient]:
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()


def create_patient(db: Session, patient: schemas.PatientCreate) -> models.Patient:
    db_patient = models.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(db: Session, patient_id: str, patient: schemas.PatientUpdate) -> Optional[models.Patient]:
    db_patient = get_patient(db, patient_id)
    if db_patient:
        update_data = patient.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_patient, key, value)
        db.commit()
        db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: str) -> bool:
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db.delete(db_patient)
        db.commit()
        return True
    return False


# ========== DOCTOR CRUD ==========
def get_doctors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Doctor]:
    return db.query(models.Doctor).offset(skip).limit(limit).all()


def get_doctor(db: Session, doctor_id: str) -> Optional[models.Doctor]:
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()


def create_doctor(db: Session, doctor: schemas.DoctorCreate) -> models.Doctor:
    db_doctor = models.Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def update_doctor(db: Session, doctor_id: str, doctor: schemas.DoctorUpdate) -> Optional[models.Doctor]:
    db_doctor = get_doctor(db, doctor_id)
    if db_doctor:
        update_data = doctor.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_doctor, key, value)
        db.commit()
        db.refresh(db_doctor)
    return db_doctor


def delete_doctor(db: Session, doctor_id: str) -> bool:
    db_doctor = get_doctor(db, doctor_id)
    if db_doctor:
        db.delete(db_doctor)
        db.commit()
        return True
    return False


# ========== APPOINTMENT CRUD ==========
def get_appointments(db: Session, skip: int = 0, limit: int = 100) -> List[models.Appointment]:
    appointments = db.query(models.Appointment).offset(skip).limit(limit).all()
    
    # Add patient and doctor names
    for appointment in appointments:
        if appointment.patient:
            appointment.patient_name = appointment.patient.name
        if appointment.doctor:
            appointment.doctor_name = appointment.doctor.name
    
    return appointments


def get_appointment(db: Session, appointment_id: str) -> Optional[models.Appointment]:
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    
    if appointment:
        if appointment.patient:
            appointment.patient_name = appointment.patient.name
        if appointment.doctor:
            appointment.doctor_name = appointment.doctor.name
    
    return appointment


def create_appointment(db: Session, appointment: schemas.AppointmentCreate) -> models.Appointment:
    db_appointment = models.Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    
    # Add patient and doctor names
    if db_appointment.patient:
        db_appointment.patient_name = db_appointment.patient.name
    if db_appointment.doctor:
        db_appointment.doctor_name = db_appointment.doctor.name
    
    return db_appointment


def update_appointment(db: Session, appointment_id: str, appointment: schemas.AppointmentUpdate) -> Optional[models.Appointment]:
    db_appointment = get_appointment(db, appointment_id)
    if db_appointment:
        update_data = appointment.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_appointment, key, value)
        db.commit()
        db.refresh(db_appointment)
        
        # Add patient and doctor names
        if db_appointment.patient:
            db_appointment.patient_name = db_appointment.patient.name
        if db_appointment.doctor:
            db_appointment.doctor_name = db_appointment.doctor.name
    
    return db_appointment


def delete_appointment(db: Session, appointment_id: str) -> bool:
    db_appointment = get_appointment(db, appointment_id)
    if db_appointment:
        db.delete(db_appointment)
        db.commit()
        return True
    return False


# ========== PRESCRIPTION CRUD ==========
def get_prescriptions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Prescription]:
    prescriptions = db.query(models.Prescription).offset(skip).limit(limit).all()
    
    # Add patient and doctor names
    for prescription in prescriptions:
        if prescription.patient:
            prescription.patient_name = prescription.patient.name
        if prescription.doctor:
            prescription.doctor_name = prescription.doctor.name
    
    return prescriptions


def get_prescription(db: Session, prescription_id: str) -> Optional[models.Prescription]:
    prescription = db.query(models.Prescription).filter(models.Prescription.id == prescription_id).first()
    
    if prescription:
        if prescription.patient:
            prescription.patient_name = prescription.patient.name
        if prescription.doctor:
            prescription.doctor_name = prescription.doctor.name
    
    return prescription


def get_prescriptions_by_patient(db: Session, patient_id: str) -> List[models.Prescription]:
    prescriptions = db.query(models.Prescription).filter(models.Prescription.patient_id == patient_id).all()
    
    # Add patient and doctor names
    for prescription in prescriptions:
        if prescription.patient:
            prescription.patient_name = prescription.patient.name
        if prescription.doctor:
            prescription.doctor_name = prescription.doctor.name
    
    return prescriptions


def create_prescription(db: Session, prescription: schemas.PrescriptionCreate) -> models.Prescription:
    prescription_data = prescription.model_dump()
    
    # Convert attachments list to string if present
    if prescription_data.get('attachments'):
        prescription_data['attachments'] = ','.join(prescription_data['attachments'])
    
    db_prescription = models.Prescription(**prescription_data)
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    
    # Add patient and doctor names
    if db_prescription.patient:
        db_prescription.patient_name = db_prescription.patient.name
    if db_prescription.doctor:
        db_prescription.doctor_name = db_prescription.doctor.name
    
    return db_prescription


def update_prescription(db: Session, prescription_id: str, prescription: schemas.PrescriptionUpdate) -> Optional[models.Prescription]:
    db_prescription = get_prescription(db, prescription_id)
    if db_prescription:
        update_data = prescription.model_dump(exclude_unset=True)
        
        # Convert attachments list to string if present
        if 'attachments' in update_data and update_data['attachments']:
            update_data['attachments'] = ','.join(update_data['attachments'])
        
        for key, value in update_data.items():
            setattr(db_prescription, key, value)
        db.commit()
        db.refresh(db_prescription)
        
        # Add patient and doctor names
        if db_prescription.patient:
            db_prescription.patient_name = db_prescription.patient.name
        if db_prescription.doctor:
            db_prescription.doctor_name = db_prescription.doctor.name
    
    return db_prescription


def delete_prescription(db: Session, prescription_id: str) -> bool:
    db_prescription = get_prescription(db, prescription_id)
    if db_prescription:
        db.delete(db_prescription)
        db.commit()
        return True
    return False


# ========== DASHBOARD STATS ==========
def get_dashboard_stats(db: Session) -> schemas.DashboardStats:
    # Total patients
    total_patients = db.query(func.count(models.Patient.id)).scalar() or 0
    
    # Total appointments
    total_appointments = db.query(func.count(models.Appointment.id)).scalar() or 0
    
    # Active prescriptions (all prescriptions)
    active_prescriptions = db.query(func.count(models.Prescription.id)).scalar() or 0
    
    # Today's appointments
    today = date.today()
    today_appointments = db.query(func.count(models.Appointment.id)).filter(
        models.Appointment.date == today
    ).scalar() or 0
    
    return schemas.DashboardStats(
        total_patients=total_patients,
        total_appointments=total_appointments,
        active_prescriptions=active_prescriptions,
        today_appointments=today_appointments
    )
















