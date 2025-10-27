"""
Seed script to populate the database with sample data
"""
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
import models
from datetime import date, time


def seed_database():
    """Populate database with sample data"""
    
    # Initialize database
    init_db()
    
    db: Session = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(models.Patient).first():
            print("⚠️  Database already contains data. Skipping seed.")
            return
        
        print("🌱 Seeding database...")
        
        # Create Doctors
        doctors = [
            models.Doctor(
                name="Sarah Williams",
                specialization="Cardiology",
                contact="+1234560001",
                email="sarah.williams@hospital.com"
            ),
            models.Doctor(
                name="Michael Brown",
                specialization="General Medicine",
                contact="+1234560002",
                email="michael.brown@hospital.com"
            ),
            models.Doctor(
                name="Lisa Anderson",
                specialization="Neurology",
                contact="+1234560003",
                email="lisa.anderson@hospital.com"
            ),
            models.Doctor(
                name="James Wilson",
                specialization="Orthopedics",
                contact="+1234560004",
                email="james.wilson@hospital.com"
            ),
        ]
        
        db.add_all(doctors)
        db.commit()
        print("✅ Added 4 doctors")
        
        # Create Patients
        patients = [
            models.Patient(
                name="John Doe",
                age=35,
                gender="Male",
                contact="+1234567890",
                address="123 Main St, City, State",
                medical_history="Hypertension, Type 2 Diabetes"
            ),
            models.Patient(
                name="Jane Smith",
                age=28,
                gender="Female",
                contact="+1234567891",
                address="456 Oak Ave, City, State",
                medical_history="Asthma"
            ),
            models.Patient(
                name="Robert Johnson",
                age=52,
                gender="Male",
                contact="+1234567892",
                address="789 Pine Rd, City, State",
                medical_history="Heart Disease, High Cholesterol"
            ),
            models.Patient(
                name="Emily Davis",
                age=41,
                gender="Female",
                contact="+1234567893",
                address="321 Elm St, City, State",
                medical_history="Migraine, Anxiety"
            ),
        ]
        
        db.add_all(patients)
        db.commit()
        print("✅ Added 4 patients")
        
        # Refresh to get IDs
        for doctor in doctors:
            db.refresh(doctor)
        for patient in patients:
            db.refresh(patient)
        
        # Create Appointments
        appointments = [
            models.Appointment(
                patient_id=patients[0].id,
                doctor_id=doctors[0].id,
                date=date(2024, 10, 25),
                time=time(10, 0),
                reason="Regular checkup for hypertension",
                status="Scheduled"
            ),
            models.Appointment(
                patient_id=patients[1].id,
                doctor_id=doctors[1].id,
                date=date(2024, 10, 24),
                time=time(14, 30),
                reason="Asthma follow-up",
                status="Scheduled"
            ),
            models.Appointment(
                patient_id=patients[2].id,
                doctor_id=doctors[0].id,
                date=date(2024, 10, 20),
                time=time(11, 0),
                reason="Cardiac consultation",
                status="Completed"
            ),
            models.Appointment(
                patient_id=patients[3].id,
                doctor_id=doctors[2].id,
                date=date(2024, 10, 26),
                time=time(15, 0),
                reason="Migraine treatment",
                status="Scheduled"
            ),
        ]
        
        db.add_all(appointments)
        db.commit()
        print("✅ Added 4 appointments")
        
        # Create Prescriptions
        prescriptions = [
            models.Prescription(
                patient_id=patients[0].id,
                doctor_id=doctors[0].id,
                diagnosis="Hypertension",
                medications="Lisinopril 10mg - Once daily, Amlodipine 5mg - Once daily",
                instructions="Take medications with food. Monitor blood pressure daily.",
                date=date(2024, 10, 20)
            ),
            models.Prescription(
                patient_id=patients[1].id,
                doctor_id=doctors[1].id,
                diagnosis="Acute Asthma Exacerbation",
                medications="Albuterol inhaler - As needed, Fluticasone 250mcg - Twice daily",
                instructions="Use rescue inhaler for breathing difficulty. Avoid allergens.",
                date=date(2024, 10, 18)
            ),
            models.Prescription(
                patient_id=patients[2].id,
                doctor_id=doctors[0].id,
                diagnosis="High Cholesterol",
                medications="Atorvastatin 20mg - Once daily at bedtime",
                instructions="Follow low-cholesterol diet. Exercise regularly. Recheck lipids in 3 months.",
                date=date(2024, 10, 20)
            ),
        ]
        
        db.add_all(prescriptions)
        db.commit()
        print("✅ Added 3 prescriptions")
        
        print("🎉 Database seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()






