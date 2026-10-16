from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from .db import Base

class AppointmentStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Mentor(Base):
    __tablename__ = "mentors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    department = Column(String(100), nullable=False, index=True)
    expertise_areas = Column(String(255), nullable=False) # e.g. "DevOps, Cloud, Python, DSA"
    max_daily_slots = Column(Integer, default=4)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    slots = relationship("Slot", back_populates="mentor", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="mentor", cascade="all, delete-orphan")

class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, ForeignKey("mentors.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    is_booked = Column(Boolean, default=False, nullable=False)
    location_or_link = Column(String(255), default="Meet / Room 402")
    created_at = Column(DateTime, default=datetime.utcnow)

    mentor = relationship("Mentor", back_populates="slots")
    appointment = relationship("Appointment", back_populates="slot", uselist=False)

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    slot_id = Column(Integer, ForeignKey("slots.id", ondelete="CASCADE"), nullable=False, unique=True)
    mentor_id = Column(Integer, ForeignKey("mentors.id", ondelete="CASCADE"), nullable=False)
    student_name = Column(String(100), nullable=False)
    student_email = Column(String(120), nullable=False)
    student_roll = Column(String(50), nullable=False, index=True)
    topic = Column(String(200), nullable=False)
    status = Column(String(20), default=AppointmentStatus.CONFIRMED.value, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    slot = relationship("Slot", back_populates="appointment")
    mentor = relationship("Mentor", back_populates="appointments")
