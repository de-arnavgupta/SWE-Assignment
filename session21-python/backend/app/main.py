from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select, func, text
from typing import List, Optional
from prometheus_fastapi_instrumentator import Instrumentator

from .config import settings
from .db import get_db, engine, Base
from .models import Mentor, Slot, Appointment, AppointmentStatus
from .schemas import (
    MentorCreate, MentorResponse,
    SlotCreate, SlotResponse,
    AppointmentCreate, AppointmentResponse, AppointmentStatusUpdate,
    StatsSummary
)

# Initialize FastAPI application
app = FastAPI(
    title="MentorSync API",
    description="Office Hours & Peer Tutoring Appointment Booking System",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expose Prometheus /metrics endpoint
Instrumentator().instrument(app).expose(app)

# Ensure tables exist on startup (for SQLite/test compatibility)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# --- Core Health & Readiness Probes ---

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "mentorsync-api",
        "student": "Arnav Gupta",
        "roll": "24bcs10063"
    }

@app.get("/ready", tags=["Health"])
def readiness_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error: {str(e)}"
        )

# --- Mentors REST Endpoints ---

@app.get("/api/v1/mentors", response_model=List[MentorResponse], tags=["Mentors"])
def list_mentors(
    department: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = select(Mentor)
    if department:
        query = query.where(Mentor.department.ilike(f"%{department}%"))
    if search:
        query = query.where(
            (Mentor.name.ilike(f"%{search}%")) |
            (Mentor.expertise_areas.ilike(f"%{search}%"))
        )
    return db.scalars(query).all()

@app.post("/api/v1/mentors", response_model=MentorResponse, status_code=status.HTTP_201_CREATED, tags=["Mentors"])
def create_mentor(mentor_in: MentorCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(Mentor).where(Mentor.email == mentor_in.email))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Mentor with email '{mentor_in.email}' already registered."
        )
    mentor = Mentor(**mentor_in.model_dump())
    db.add(mentor)
    db.commit()
    db.refresh(mentor)
    return mentor

@app.get("/api/v1/mentors/{mentor_id}", response_model=MentorResponse, tags=["Mentors"])
def get_mentor(mentor_id: int, db: Session = Depends(get_db)):
    mentor = db.get(Mentor, mentor_id)
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mentor with ID {mentor_id} not found."
        )
    return mentor

@app.delete("/api/v1/mentors/{mentor_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Mentors"])
def delete_mentor(mentor_id: int, db: Session = Depends(get_db)):
    mentor = db.get(Mentor, mentor_id)
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mentor with ID {mentor_id} not found."
        )
    db.delete(mentor)
    db.commit()
    return None

# --- Slots REST Endpoints ---

@app.post("/api/v1/mentors/{mentor_id}/slots", response_model=SlotResponse, status_code=status.HTTP_201_CREATED, tags=["Slots"])
def create_slot(mentor_id: int, slot_in: SlotCreate, db: Session = Depends(get_db)):
    mentor = db.get(Mentor, mentor_id)
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mentor with ID {mentor_id} not found."
        )
    if slot_in.end_time <= slot_in.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot end_time must be chronologically after start_time."
        )
    slot = Slot(mentor_id=mentor_id, **slot_in.model_dump())
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot

# --- Appointments REST Endpoints (GET, POST, PUT, DELETE) ---

@app.get("/api/v1/appointments", response_model=List[AppointmentResponse], tags=["Appointments"])
def list_appointments(
    status: Optional[str] = None,
    student_roll: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = select(Appointment)
    if status:
        query = query.where(Appointment.status == status.upper())
    if student_roll:
        query = query.where(Appointment.student_roll == student_roll)
    return db.scalars(query).all()

@app.post("/api/v1/appointments", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED, tags=["Appointments"])
def book_appointment(appt_in: AppointmentCreate, db: Session = Depends(get_db)):
    # 1. Verify slot exists
    slot = db.get(Slot, appt_in.slot_id)
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slot with ID {appt_in.slot_id} not found."
        )
    # 2. Prevent double booking conflict
    if slot.is_booked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This slot is already booked. Please choose an available time slot."
        )
    # 3. Verify mentor match
    if slot.mentor_id != appt_in.mentor_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot does not belong to the specified mentor."
        )

    # 4. Atomic booking state transition
    slot.is_booked = True
    appointment = Appointment(
        slot_id=appt_in.slot_id,
        mentor_id=appt_in.mentor_id,
        student_name=appt_in.student_name,
        student_email=appt_in.student_email,
        student_roll=appt_in.student_roll,
        topic=appt_in.topic,
        status=AppointmentStatus.CONFIRMED.value,
        notes=appt_in.notes
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

@app.put("/api/v1/appointments/{appointment_id}/status", response_model=AppointmentResponse, tags=["Appointments"])
def update_appointment_status(
    appointment_id: int,
    status_update: AppointmentStatusUpdate,
    db: Session = Depends(get_db)
):
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {appointment_id} not found."
        )
    
    new_status = status_update.status.upper()
    old_status = appointment.status
    appointment.status = new_status

    # Business rule: If cancelled, free the slot for other students!
    if new_status == AppointmentStatus.CANCELLED.value and appointment.slot:
        appointment.slot.is_booked = False
    elif old_status == AppointmentStatus.CANCELLED.value and new_status == AppointmentStatus.CONFIRMED.value and appointment.slot:
        appointment.slot.is_booked = True

    db.commit()
    db.refresh(appointment)
    return appointment

@app.delete("/api/v1/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Appointments"])
def cancel_and_delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {appointment_id} not found."
        )
    if appointment.slot:
        appointment.slot.is_booked = False
    db.delete(appointment)
    db.commit()
    return None

# --- Summary Statistics Endpoint ---

@app.get("/api/v1/stats/summary", response_model=StatsSummary, tags=["Analytics"])
def get_stats_summary(db: Session = Depends(get_db)):
    total_mentors = db.scalar(select(func.count(Mentor.id))) or 0
    total_slots = db.scalar(select(func.count(Slot.id))) or 0
    available_slots = db.scalar(select(func.count(Slot.id)).where(Slot.is_booked == False)) or 0
    total_appts = db.scalar(select(func.count(Appointment.id))) or 0
    confirmed = db.scalar(select(func.count(Appointment.id)).where(Appointment.status == AppointmentStatus.CONFIRMED.value)) or 0
    completed = db.scalar(select(func.count(Appointment.id)).where(Appointment.status == AppointmentStatus.COMPLETED.value)) or 0
    cancelled = db.scalar(select(func.count(Appointment.id)).where(Appointment.status == AppointmentStatus.CANCELLED.value)) or 0

    return StatsSummary(
        total_mentors=total_mentors,
        total_slots=total_slots,
        available_slots=available_slots,
        total_appointments=total_appts,
        confirmed_appointments=confirmed,
        completed_appointments=completed,
        cancelled_appointments=cancelled
    )
