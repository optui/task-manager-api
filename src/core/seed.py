from datetime import datetime, timedelta
from src.tasks.models import Task, TaskStatus
from src.core.database import Base, SessionLocal, engine

# Connect and initialize database session
db = SessionLocal()

# Sample seed data
tasks = [
    Task(
        title="Project Alpha Review",
        description="Initial assessment of Project Alpha.",
        due_date=(datetime.now() + timedelta(days=1)).date(),
        status=TaskStatus.completed,
    ),
    Task(
        title="Project Alpha Follow-up Meeting",
        description="Follow-up meeting to discuss Project Alpha progress.",
        due_date=(datetime.now() + timedelta(days=2)).date(),
        status=TaskStatus.completed,
    ),
    Task(
        title="Project Alpha Finalization",
        description="Finalization of Project Alpha deliverables.",
        due_date=(datetime.now() + timedelta(days=3)).date(),
        status=TaskStatus.completed,
    ),
    Task(
        title="Project Beta Review",
        description="Initial assessment of Project Beta.",
        due_date=(datetime.now() + timedelta(days=7)).date(),
        status=TaskStatus.completed,
    ),
    Task(
        title="Project Beta Follow-up Meeting",
        description="Follow-up meeting for Project Beta to review progress.",
        due_date=(datetime.now() + timedelta(days=8)).date(),
        status=TaskStatus.completed,
    ),
    Task(
        title="Project Gamma Review",
        description="Initial assessment of Project Gamma.",
        due_date=(datetime.now() + timedelta(days=14)).date(),
        status=TaskStatus.completed,
    ),
]

# Seed data into the database
try:
    print("Seeding database...")
    Base.metadata.create_all(bind=engine)

    existing_task = db.query(Task).first()
    if existing_task is None:
        db.add_all(tasks)
        db.commit()
        print("✅ Database seeded successfully.")
    else:
        print("✅ Database already contains data. Skipping seeding.")

except Exception as e:
    db.rollback()
    print(f"❌ Database seeding failed: {e}")

finally:
    db.close()
    print("✅ Database session closed.")
