from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

# --- Slot Schemas ---
class SlotBase(BaseModel):
    start_time: datetime
    end_time: datetime
    location_or_link: Optional[str] = "Online / Meet Link"

class SlotCreate(SlotBase):
    pass

class SlotResponse(SlotBase):
    id: int
    mentor_id: int
    is_booked: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Mentor Schemas ---
class MentorBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    department: str = Field(..., min_length=2, max_length=100)
    expertise_areas: str = Field(..., min_length=2, max_length=255)
    max_daily_slots: Optional[int] = Field(default=4, ge=1, le=12)
    bio: Optional[str] = None

class MentorCreate(MentorBase):
    pass

class MentorResponse(MentorBase):
    id: int
    created_at: datetime
    slots: List[SlotResponse] = []

    model_config = ConfigDict(from_attributes=True)

# --- Appointment Schemas ---
class AppointmentBase(BaseModel):
    slot_id: int
    mentor_id: int
    student_name: str = Field(..., min_length=2, max_length=100)
    student_email: EmailStr
    student_roll: str = Field(..., min_length=3, max_length=50)
    topic: str = Field(..., min_length=3, max_length=200)
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(PENDING|CONFIRMED|COMPLETED|CANCELLED)$")

class AppointmentResponse(AppointmentBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Summary Stats Schema ---
class StatsSummary(BaseModel):
    total_mentors: int
    total_slots: int
    available_slots: int
    total_appointments: int
    confirmed_appointments: int
    completed_appointments: int
    cancelled_appointments: int
