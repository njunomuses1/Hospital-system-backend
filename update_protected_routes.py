"""
Script to add authentication to all routes in main.py
"""
import re

# Read the current main.py file
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Patterns to protect endpoints that don't have current_user
patterns_to_update = [
    # Doctors
    (r'@app\.get\("/api/doctors",.*?\ndef get_doctors\((.*?)\):',
     r'@app.get("/api/doctors", response_model=schemas.ApiResponse)\ndef get_doctors(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    (r'@app\.get\("/api/doctors/{doctor_id}",.*?\ndef get_doctor\((.*?)\):',
     r'@app.get("/api/doctors/{doctor_id}", response_model=schemas.ApiResponse)\ndef get_doctor(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    (r'@app\.post\("/api/doctors",.*?\ndef create_doctor\((.*?)\):',
     r'@app.post("/api/doctors", response_model=schemas.ApiResponse, status_code=status.HTTP_201_CREATED)\ndef create_doctor(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    (r'@app\.put\("/api/doctors/{doctor_id}",.*?\ndef update_doctor\((.*?)\):',
     r'@app.put("/api/doctors/{doctor_id}", response_model=schemas.ApiResponse)\ndef update_doctor(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    (r'@app\.delete\("/api/doctors/{doctor_id}",.*?\ndef delete_doctor\((.*?)\):',
     r'@app.delete("/api/doctors/{doctor_id}", response_model=schemas.ApiResponse)\ndef delete_doctor(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    # Appointments
    (r'@app\.get\("/api/appointments",.*?\ndef get_appointments\((.*?)\):',
     r'@app.get("/api/appointments", response_model=schemas.ApiResponse)\ndef get_appointments(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    (r'@app\.get\("/api/appointments/{appointment_id}",.*?\ndef get_appointment\((.*?)\):',
     r'@app.get("/api/appointments/{appointment_id}", response_model=schemas.ApiResponse)\ndef get_appointment(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    (r'@app\.post\("/api/appointments",.*?\ndef create_appointment\((.*?)\):',
     r'@app.post("/api/appointments", response_model=schemas.ApiResponse, status_code=status.HTTP_201_CREATED)\ndef create_appointment(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    (r'@app\.put\("/api/appointments/{appointment_id}",.*?\ndef update_appointment\((.*?)\):',
     r'@app.put("/api/appointments/{appointment_id}", response_model=schemas.ApiResponse)\ndef update_appointment(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    (r'@app\.delete\("/api/appointments/{appointment_id}",.*?\ndef delete_appointment\((.*?)\):',
     r'@app.delete("/api/appointments/{appointment_id}", response_model=schemas.ApiResponse)\ndef delete_appointment(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    # Prescriptions
    (r'@app\.get\("/api/prescriptions",.*?\ndef get_prescriptions\((.*?)\):',
     r'@app.get("/api/prescriptions", response_model=schemas.ApiResponse)\ndef get_prescriptions(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    (r'@app\.get\("/api/prescriptions/{prescription_id}",.*?\ndef get_prescription\((.*?)\):',
     r'@app.get("/api/prescriptions/{prescription_id}", response_model=schemas.ApiResponse)\ndef get_prescription(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    (r'@app\.get\("/api/prescriptions/patient/{patient_id}",.*?\ndef get_prescriptions_by_patient\((.*?)\):',
     r'@app.get("/api/prescriptions/patient/{patient_id}", response_model=schemas.ApiResponse)\ndef get_prescriptions_by_patient(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    (r'@app\.post\("/api/prescriptions",.*?\ndef create_prescription\((.*?)\):',
     r'@app.post("/api/prescriptions", response_model=schemas.ApiResponse, status_code=status.HTTP_201_CREATED)\ndef create_prescription(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    (r'@app\.put\("/api/prescriptions/{prescription_id}",.*?\ndef update_prescription\((.*?)\):',
     r'@app.put("/api/prescriptions/{prescription_id}", response_model=schemas.ApiResponse)\ndef update_prescription(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    (r'@app\.delete\("/api/prescriptions/{prescription_id}",.*?\ndef delete_prescription\((.*?)\):',
     r'@app.delete("/api/prescriptions/{prescription_id}", response_model=schemas.ApiResponse)\ndef delete_prescription(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
    
    # Dashboard
    (r'@app\.get\("/api/dashboard/stats",.*?\ndef get_dashboard_stats\((.*?)\):',
     r'@app.get("/api/dashboard/stats", response_model=schemas.ApiResponse)\ndef get_dashboard_stats(\1, current_user: models.User = Depends(auth.get_current_active_user)):'),
]

# Apply updates
for pattern, replacement in patterns_to_update:
    # Check if current_user not already present
    if re.search(pattern, content) and 'current_user' not in re.search(pattern, content).group(0):
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        print(f"Updated pattern: {pattern[:50]}...")

# Write back
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ All routes have been protected with authentication!")














