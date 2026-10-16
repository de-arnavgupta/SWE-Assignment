from alembic import op
import sqlalchemy as sa

revision = "0001_initial_mentorsync"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 1. Create mentors table
    op.create_table(
        "mentors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False, unique=True),
        sa.Column("department", sa.String(length=100), nullable=False),
        sa.Column("expertise_areas", sa.String(length=255), nullable=False),
        sa.Column("max_daily_slots", sa.Integer(), nullable=False, server_default="4"),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_mentors_name", "mentors", ["name"])
    op.create_index("ix_mentors_department", "mentors", ["department"])

    # 2. Create slots table
    op.create_table(
        "slots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mentor_id", sa.Integer(), sa.ForeignKey("mentors.id", ondelete="CASCADE"), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.Column("is_booked", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("location_or_link", sa.String(length=255), nullable=False, server_default="Online / Meet Link"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_slots_start_time", "slots", ["start_time"])

    # 3. Create appointments table
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slot_id", sa.Integer(), sa.ForeignKey("slots.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("mentor_id", sa.Integer(), sa.ForeignKey("mentors.id", ondelete="CASCADE"), nullable=False),
        sa.Column("student_name", sa.String(length=100), nullable=False),
        sa.Column("student_email", sa.String(length=120), nullable=False),
        sa.Column("student_roll", sa.String(length=50), nullable=False),
        sa.Column("topic", sa.String(length=200), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="CONFIRMED"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_appointments_student_roll", "appointments", ["student_roll"])
    op.create_index("ix_appointments_status", "appointments", ["status"])

def downgrade():
    op.drop_table("appointments")
    op.drop_table("slots")
    op.drop_table("mentors")
