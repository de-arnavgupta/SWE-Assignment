import pytest
from datetime import datetime, timedelta

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "mentorsync-api"
    assert data["student"] == "Arnav Gupta"
    assert data["roll"] == "24bcs10063"

def test_readiness_check(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready", "database": "connected"}

def test_create_mentor_success(client):
    payload = {
        "name": "Dr. Sarah Connor",
        "email": "sarah.connor@university.edu",
        "department": "Computer Science",
        "expertise_areas": "Cloud Architecture, Kubernetes, Distributed Systems",
        "max_daily_slots": 4,
        "bio": "Research associate focusing on distributed consensus protocols."
    }
    response = client.post("/api/v1/mentors", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["department"] == payload["department"]

def test_create_mentor_duplicate_email(client):
    payload = {
        "name": "Prof. Alan Turing",
        "email": "alan.turing@university.edu",
        "department": "Mathematics",
        "expertise_areas": "Theoretical Computation"
    }
    res1 = client.post("/api/v1/mentors", json=payload)
    assert res1.status_code == 201

    # Attempt duplicate registration
    res2 = client.post("/api/v1/mentors", json=payload)
    assert res2.status_code == 400
    assert "already registered" in res2.json()["detail"]

def test_create_mentor_validation_error(client):
    # Invalid email address format
    payload = {
        "name": "Invalid User",
        "email": "not-an-email",
        "department": "Engineering",
        "expertise_areas": "Hardware"
    }
    response = client.post("/api/v1/mentors", json=payload)
    assert response.status_code == 422 # Pydantic validation rejection

def test_list_and_filter_mentors(client):
    client.post("/api/v1/mentors", json={
        "name": "Alice Smith",
        "email": "alice@univ.edu",
        "department": "Data Science",
        "expertise_areas": "Python, Machine Learning"
    })
    client.post("/api/v1/mentors", json={
        "name": "Bob Jones",
        "email": "bob@univ.edu",
        "department": "Software Engineering",
        "expertise_areas": "DevOps, Terraform, AWS"
    })

    # Filter by department
    res_ds = client.get("/api/v1/mentors?department=Data Science")
    assert res_ds.status_code == 200
    mentors_ds = res_ds.json()
    assert len(mentors_ds) == 1
    assert mentors_ds[0]["name"] == "Alice Smith"

    # Search by keyword
    res_search = client.get("/api/v1/mentors?search=Terraform")
    assert res_search.status_code == 200
    mentors_search = res_search.json()
    assert len(mentors_search) == 1
    assert mentors_search[0]["name"] == "Bob Jones"

def test_create_and_validate_slot(client):
    # Create mentor
    mentor_res = client.post("/api/v1/mentors", json={
        "name": "Grace Hopper",
        "email": "grace@univ.edu",
        "department": "Computer Science",
        "expertise_areas": "Compilers"
    })
    mentor_id = mentor_res.json()["id"]

    now = datetime.utcnow()
    slot_payload = {
        "start_time": (now + timedelta(hours=1)).isoformat(),
        "end_time": (now + timedelta(hours=2)).isoformat(),
        "location_or_link": "Room 301 / Google Meet"
    }
    res = client.post(f"/api/v1/mentors/{mentor_id}/slots", json=slot_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["mentor_id"] == mentor_id
    assert data["is_booked"] is False

    # Invalid chronological range (end_time before start_time)
    invalid_slot = {
        "start_time": (now + timedelta(hours=2)).isoformat(),
        "end_time": (now + timedelta(hours=1)).isoformat()
    }
    inv_res = client.post(f"/api/v1/mentors/{mentor_id}/slots", json=invalid_slot)
    assert inv_res.status_code == 400

def test_book_appointment_and_prevent_double_booking(client):
    # 1. Create mentor
    m_res = client.post("/api/v1/mentors", json={
        "name": "Linus Torvalds",
        "email": "linus@univ.edu",
        "department": "Systems",
        "expertise_areas": "Linux Kernel, C, Git"
    })
    mentor_id = m_res.json()["id"]

    # 2. Create slot
    now = datetime.utcnow()
    s_res = client.post(f"/api/v1/mentors/{mentor_id}/slots", json={
        "start_time": (now + timedelta(days=1)).isoformat(),
        "end_time": (now + timedelta(days=1, hours=1)).isoformat()
    })
    slot_id = s_res.json()["id"]

    # 3. Book slot (Happy path)
    booking_payload = {
        "slot_id": slot_id,
        "mentor_id": mentor_id,
        "student_name": "Arnav Gupta",
        "student_email": "arnav.24bcs10063@sst.scaler.com",
        "student_roll": "24bcs10063",
        "topic": "Kubernetes CNI & CoreDNS Debugging",
        "notes": "Need guidance on pod networking troubleshooting."
    }
    b_res = client.post("/api/v1/appointments", json=booking_payload)
    assert b_res.status_code == 201
    appt_data = b_res.json()
    assert appt_data["id"] is not None
    assert appt_data["status"] == "CONFIRMED"
    assert appt_data["student_roll"] == "24bcs10063"

    # 4. Attempt double booking on the same slot (MUST FAIL with 400)
    conflict_payload = {
        "slot_id": slot_id,
        "mentor_id": mentor_id,
        "student_name": "Second Student",
        "student_email": "student2@sst.scaler.com",
        "student_roll": "24bcs10999",
        "topic": "Linux basics"
    }
    conflict_res = client.post("/api/v1/appointments", json=conflict_payload)
    assert conflict_res.status_code == 400
    assert "already booked" in conflict_res.json()["detail"]

def test_appointment_status_transition_and_slot_release(client):
    # Create mentor, slot, and appointment
    m_res = client.post("/api/v1/mentors", json={
        "name": "Dennis Ritchie",
        "email": "dennis@univ.edu",
        "department": "Systems",
        "expertise_areas": "C, Unix"
    })
    mentor_id = m_res.json()["id"]

    now = datetime.utcnow()
    s_res = client.post(f"/api/v1/mentors/{mentor_id}/slots", json={
        "start_time": (now + timedelta(days=2)).isoformat(),
        "end_time": (now + timedelta(days=2, hours=1)).isoformat()
    })
    slot_id = s_res.json()["id"]

    appt_res = client.post("/api/v1/appointments", json={
        "slot_id": slot_id,
        "mentor_id": mentor_id,
        "student_name": "Arnav Gupta",
        "student_email": "arnav.24bcs10063@sst.scaler.com",
        "student_roll": "24bcs10063",
        "topic": "C memory management"
    })
    appt_id = appt_res.json()["id"]

    # 1. Update to COMPLETED
    up_res = client.put(f"/api/v1/appointments/{appt_id}/status", json={"status": "COMPLETED"})
    assert up_res.status_code == 200
    assert up_res.json()["status"] == "COMPLETED"

    # 2. Update to CANCELLED -> Verify slot is automatically freed!
    cancel_res = client.put(f"/api/v1/appointments/{appt_id}/status", json={"status": "CANCELLED"})
    assert cancel_res.status_code == 200
    assert cancel_res.json()["status"] == "CANCELLED"

    # Verify slot availability in mentor profile
    mentor_view = client.get(f"/api/v1/mentors/{mentor_id}").json()
    freed_slot = next(s for s in mentor_view["slots"] if s["id"] == slot_id)
    assert freed_slot["is_booked"] is False # Slot released!

def test_stats_summary_endpoint(client):
    res = client.get("/api/v1/stats/summary")
    assert res.status_code == 200
    data = res.json()
    assert "total_mentors" in data
    assert "total_appointments" in data
    assert "available_slots" in data
