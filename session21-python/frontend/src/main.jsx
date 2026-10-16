import React, { useState, useEffect, useCallback } from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css';

// Fallback seed data if backend is in provisioning phase
const SEED_MENTORS = [
  {
    id: 1,
    name: "Dr. Sarah Connor",
    email: "sarah.connor@university.edu",
    department: "Computer Science",
    expertise_areas: "Distributed Systems, Kubernetes, Cloud Architecture",
    bio: "Senior Researcher with 10+ years in distributed systems and cloud native architectures.",
    slots: [
      { id: 101, mentor_id: 1, start_time: "2026-10-18T10:00:00Z", end_time: "2026-10-18T11:00:00Z", is_booked: false, location_or_link: "Room 402 / Meet" },
      { id: 102, mentor_id: 1, start_time: "2026-10-18T14:00:00Z", end_time: "2026-10-18T15:00:00Z", is_booked: true, location_or_link: "Google Meet" }
    ]
  },
  {
    id: 2,
    name: "Prof. Alan Turing",
    email: "alan.turing@university.edu",
    department: "Software Engineering",
    expertise_areas: "Algorithms, Python, System Design",
    bio: "Passionate about discrete algorithms, software verification, and scalable clean code.",
    slots: [
      { id: 201, mentor_id: 2, start_time: "2026-10-19T11:00:00Z", end_time: "2026-10-19T12:00:00Z", is_booked: false, location_or_link: "Virtual Room A" }
    ]
  },
  {
    id: 3,
    name: "DevOps Engineer Alex",
    email: "alex.devops@university.edu",
    department: "DevOps & Cloud",
    expertise_areas: "Docker, Terraform, CI/CD, Prometheus",
    bio: "DevOps lead mentoring students on automated deployment pipelines and cloud resilience.",
    slots: [
      { id: 301, mentor_id: 3, start_time: "2026-10-20T15:00:00Z", end_time: "2026-10-20T16:00:00Z", is_booked: false, location_or_link: "Lab 3B / Zoom" }
    ]
  }
];

const SEED_APPOINTMENTS = [
  {
    id: 1,
    slot_id: 102,
    mentor_id: 1,
    student_name: "Arnav Gupta",
    student_email: "arnav.24bcs10063@sst.scaler.com",
    student_roll: "24bcs10063",
    topic: "Kubernetes CoreDNS & Pod Troubleshooting",
    status: "CONFIRMED",
    notes: "Reviewing assignment 14 and final capstone architecture.",
    created_at: "2026-10-16T10:00:00Z"
  }
];

function App() {
  const [mentors, setMentors] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [stats, setStats] = useState({ total_mentors: 0, available_slots: 0, total_appointments: 0, confirmed_appointments: 0 });
  const [backendOnline, setBackendOnline] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedDept, setSelectedDept] = useState("ALL");
  const [filterStatus, setFilterStatus] = useState("ALL");
  
  // Modals
  const [bookingModal, setBookingModal] = useState({ open: false, mentor: null, slot: null });
  const [bookingForm, setBookingForm] = useState({ student_name: "", student_email: "", student_roll: "", topic: "", notes: "" });
  const [newMentorModal, setNewMentorModal] = useState(false);
  const [mentorForm, setMentorForm] = useState({ name: "", email: "", department: "Computer Science", expertise_areas: "", bio: "" });

  const fetchBackendData = useCallback(async () => {
    try {
      const healthRes = await fetch("/health");
      if (healthRes.ok) {
        setBackendOnline(true);
        const [mRes, aRes, sRes] = await Promise.all([
          fetch("/api/v1/mentors"),
          fetch("/api/v1/appointments"),
          fetch("/api/v1/stats/summary")
        ]);
        if (mRes.ok) setMentors(await mRes.json());
        if (aRes.ok) setAppointments(await aRes.json());
        if (sRes.ok) setStats(await sRes.json());
        return;
      }
    } catch {
      // Backend not running on same origin, fallback to local state
    }
    setBackendOnline(false);
    setMentors(SEED_MENTORS);
    setAppointments(SEED_APPOINTMENTS);
    setStats({ total_mentors: 3, available_slots: 3, total_appointments: 1, confirmed_appointments: 1 });
  }, []);

  useEffect(() => {
    fetchBackendData();
  }, [fetchBackendData]);

  // Handle Appointment Booking
  const handleBookSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      slot_id: bookingModal.slot.id,
      mentor_id: bookingModal.mentor.id,
      ...bookingForm
    };

    if (backendOnline) {
      try {
        const res = await fetch("/api/v1/appointments", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          fetchBackendData();
          setBookingModal({ open: false, mentor: null, slot: null });
          return;
        } else {
          const err = await res.json();
          alert(`Error booking slot: ${err.detail}`);
          return;
        }
      } catch (e) {
        console.error(e);
      }
    }

    // Local state fallback
    const newAppt = { id: Date.now(), ...payload, status: "CONFIRMED", created_at: new Date().toISOString() };
    setAppointments(prev => [...prev, newAppt]);
    setMentors(prev => prev.map(m => m.id === payload.mentor_id ? {
      ...m,
      slots: m.slots.map(s => s.id === payload.slot_id ? { ...s, is_booked: true } : s)
    } : m));
    setBookingModal({ open: false, mentor: null, slot: null });
  };

  // Status transition (Completed / Cancelled)
  const handleUpdateStatus = async (apptId, newStatus) => {
    if (backendOnline) {
      try {
        await fetch(`/api/v1/appointments/${apptId}/status`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ status: newStatus })
        });
        fetchBackendData();
        return;
      } catch (e) {
        console.error(e);
      }
    }
    setAppointments(prev => prev.map(a => a.id === apptId ? { ...a, status: newStatus } : a));
  };

  // Delete appointment
  const handleDeleteAppointment = async (apptId) => {
    if (!confirm("Are you sure you want to cancel and delete this appointment?")) return;
    if (backendOnline) {
      try {
        await fetch(`/api/v1/appointments/${apptId}`, { method: "DELETE" });
        fetchBackendData();
        return;
      } catch (e) {
        console.error(e);
      }
    }
    setAppointments(prev => prev.filter(a => a.id !== apptId));
  };

  // Filtered mentors
  const filteredMentors = mentors.filter(m => {
    const matchesDept = selectedDept === "ALL" || m.department === selectedDept;
    const matchesSearch = searchQuery === "" || 
      m.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.expertise_areas.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesDept && matchesSearch;
  });

  // Filtered appointments
  const filteredAppointments = appointments.filter(a => {
    return filterStatus === "ALL" || a.status === filterStatus;
  });

  return (
    <div className="container">
      {/* Header */}
      <header className="header">
        <div className="logo-area">
          <h1>MentorSync</h1>
          <p>Office Hours & Peer Tutoring Platform — DevOps Final Capstone</p>
        </div>
        <div className="user-badge">
          <span className="pulse-dot" style={{ backgroundColor: backendOnline ? '#10b981' : '#f59e0b' }}></span>
          <span>{backendOnline ? "Live API Connected" : "Local Standalone Mode"}</span>
          <span style={{ color: '#94a3b8' }}>|</span>
          <strong>Arnav Gupta (24bcs10063)</strong>
        </div>
      </header>

      {/* KPI Cards */}
      <section className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-title">Active Mentors</div>
          <div className="kpi-value">{mentors.length}</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-title">Available Office Hour Slots</div>
          <div className="kpi-value">{stats.available_slots || mentors.reduce((acc, m) => acc + (m.slots ? m.slots.filter(s => !s.is_booked).length : 0), 0)}</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-title">Total Bookings</div>
          <div className="kpi-value">{appointments.length}</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-title">Confirmed Sessions</div>
          <div className="kpi-value">{appointments.filter(a => a.status === 'CONFIRMED').length}</div>
        </div>
      </section>

      {/* Controls Bar */}
      <div className="controls-bar">
        <input
          type="text"
          className="search-input"
          placeholder="Search mentors by name, skills, or topics (e.g. Kubernetes, DevOps)..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <select
          className="select-input"
          value={selectedDept}
          onChange={(e) => setSelectedDept(e.target.value)}
        >
          <option value="ALL">All Departments</option>
          <option value="Computer Science">Computer Science</option>
          <option value="Software Engineering">Software Engineering</option>
          <option value="DevOps & Cloud">DevOps & Cloud</option>
        </select>
        <button className="btn-primary" onClick={() => setNewMentorModal(true)}>
          + Register Mentor
        </button>
      </div>

      {/* Mentors Catalog */}
      <h2 className="section-title">Available Mentors & Office Hours</h2>
      <div className="mentor-grid">
        {filteredMentors.map(mentor => (
          <div key={mentor.id} className="mentor-card">
            <div>
              <div className="mentor-header">
                <span className="mentor-name">{mentor.name}</span>
                <span className="dept-badge">{mentor.department}</span>
              </div>
              <p className="mentor-bio">{mentor.bio || "Available for academic consultation and project guidance."}</p>
              <div className="skill-tags">
                {mentor.expertise_areas.split(',').map((tag, i) => (
                  <span key={i} className="skill-tag">{tag.trim()}</span>
                ))}
              </div>
            </div>
            
            <div style={{ marginTop: '1rem', borderTop: '1px solid #334155', paddingTop: '0.75rem' }}>
              <div style={{ fontSize: '0.8125rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                Open Time Slots:
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                {mentor.slots && mentor.slots.length > 0 ? (
                  mentor.slots.map(slot => (
                    <button
                      key={slot.id}
                      disabled={slot.is_booked}
                      onClick={() => setBookingModal({ open: true, mentor, slot })}
                      style={{
                        padding: '0.3rem 0.6rem',
                        fontSize: '0.75rem',
                        borderRadius: '4px',
                        border: '1px solid',
                        borderColor: slot.is_booked ? '#475569' : '#10b981',
                        backgroundColor: slot.is_booked ? '#1e293b' : 'rgba(16, 185, 129, 0.15)',
                        color: slot.is_booked ? '#64748b' : '#34d399',
                        cursor: slot.is_booked ? 'not-allowed' : 'pointer'
                      }}
                    >
                      {slot.is_booked ? "Booked" : "Book Slot"}
                    </button>
                  ))
                ) : (
                  <span style={{ fontSize: '0.75rem', color: '#64748b' }}>No open slots scheduled</span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Appointments Management Table */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 className="section-title" style={{ marginBottom: 0 }}>Booked Sessions & Office Hours</h2>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          {['ALL', 'CONFIRMED', 'COMPLETED', 'CANCELLED'].map(st => (
            <button
              key={st}
              onClick={() => setFilterStatus(st)}
              style={{
                background: filterStatus === st ? '#4f46e5' : '#1e293b',
                color: filterStatus === st ? 'white' : '#94a3b8',
                border: '1px solid #334155',
                padding: '0.3rem 0.75rem',
                borderRadius: '6px',
                fontSize: '0.75rem',
                cursor: 'pointer'
              }}
            >
              {st}
            </button>
          ))}
        </div>
      </div>

      <div className="appointments-section">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Student</th>
              <th>Roll Number</th>
              <th>Consultation Topic</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredAppointments.length > 0 ? (
              filteredAppointments.map(appt => (
                <tr key={appt.id}>
                  <td>#{appt.id}</td>
                  <td><strong>{appt.student_name}</strong></td>
                  <td><code>{appt.student_roll}</code></td>
                  <td>{appt.topic}</td>
                  <td>
                    <span className={`status-badge status-${appt.status}`}>
                      {appt.status}
                    </span>
                  </td>
                  <td>
                    {appt.status === 'CONFIRMED' && (
                      <button
                        className="action-btn-sm"
                        onClick={() => handleUpdateStatus(appt.id, 'COMPLETED')}
                      >
                        ✓ Complete
                      </button>
                    )}
                    {appt.status !== 'CANCELLED' && (
                      <button
                        className="action-btn-sm"
                        onClick={() => handleUpdateStatus(appt.id, 'CANCELLED')}
                      >
                        ✕ Cancel
                      </button>
                    )}
                    <button
                      className="action-btn-sm btn-danger"
                      onClick={() => handleDeleteAppointment(appt.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
                  No appointments match the selected filter.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Booking Modal */}
      {bookingModal.open && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3 className="modal-title">Book Session with {bookingModal.mentor.name}</h3>
              <button className="close-btn" onClick={() => setBookingModal({ open: false, mentor: null, slot: null })}>×</button>
            </div>
            <form onSubmit={handleBookSubmit}>
              <div className="form-group">
                <label className="form-label">Full Name</label>
                <input
                  type="text"
                  required
                  className="form-control"
                  placeholder="e.g. Arnav Gupta"
                  value={bookingForm.student_name}
                  onChange={(e) => setBookingForm({ ...bookingForm, student_name: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Student Email</label>
                <input
                  type="email"
                  required
                  className="form-control"
                  placeholder="e.g. arnav.24bcs10063@sst.scaler.com"
                  value={bookingForm.student_email}
                  onChange={(e) => setBookingForm({ ...bookingForm, student_email: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Enrollment / Roll Number</label>
                <input
                  type="text"
                  required
                  className="form-control"
                  placeholder="e.g. 24bcs10063"
                  value={bookingForm.student_roll}
                  onChange={(e) => setBookingForm({ ...bookingForm, student_roll: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Discussion Topic</label>
                <input
                  type="text"
                  required
                  className="form-control"
                  placeholder="e.g. Kubernetes Ingress and HPA Autoscaling"
                  value={bookingForm.topic}
                  onChange={(e) => setBookingForm({ ...bookingForm, topic: e.target.value })}
                />
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.5rem' }}>
                <button
                  type="button"
                  className="action-btn-sm"
                  onClick={() => setBookingModal({ open: false, mentor: null, slot: null })}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Confirm Booking
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* New Mentor Modal */}
      {newMentorModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3 className="modal-title">Register New Mentor</h3>
              <button className="close-btn" onClick={() => setNewMentorModal(false)}>×</button>
            </div>
            <form onSubmit={async (e) => {
              e.preventDefault();
              if (backendOnline) {
                try {
                  const res = await fetch("/api/v1/mentors", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(mentorForm)
                  });
                  if (res.ok) {
                    fetchBackendData();
                    setNewMentorModal(false);
                    return;
                  }
                } catch (e) {
                  console.error(e);
                }
              }
              setMentors(prev => [...prev, { id: Date.now(), ...mentorForm, slots: [] }]);
              setNewMentorModal(false);
            }}>
              <div className="form-group">
                <label className="form-label">Mentor Full Name</label>
                <input
                  type="text"
                  required
                  className="form-control"
                  placeholder="e.g. Dr. John Doe"
                  value={mentorForm.name}
                  onChange={(e) => setMentorForm({ ...mentorForm, name: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Email</label>
                <input
                  type="email"
                  required
                  className="form-control"
                  placeholder="e.g. john.doe@university.edu"
                  value={mentorForm.email}
                  onChange={(e) => setMentorForm({ ...mentorForm, email: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Department</label>
                <input
                  type="text"
                  required
                  className="form-control"
                  placeholder="e.g. Software Engineering"
                  value={mentorForm.department}
                  onChange={(e) => setMentorForm({ ...mentorForm, department: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Expertise Skills (comma-separated)</label>
                <input
                  type="text"
                  required
                  className="form-control"
                  placeholder="e.g. Cloud, Docker, Kubernetes, Python"
                  value={mentorForm.expertise_areas}
                  onChange={(e) => setMentorForm({ ...mentorForm, expertise_areas: e.target.value })}
                />
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.5rem' }}>
                <button type="button" className="action-btn-sm" onClick={() => setNewMentorModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Save Mentor
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
