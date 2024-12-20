from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
# Database setup using SQLAlchemy
DATABASE_URL = "sqlite:///./appointments.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AppointmentModel(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time_slot = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Generate available slots
def generate_slots():
    start_time = datetime.strptime("10:00 AM", "%I:%M %p")
    end_time = datetime.strptime("5:00 PM", "%I:%M %p")
    break_start = datetime.strptime("1:00 PM", "%I:%M %p")
    break_end = datetime.strptime("2:00 PM", "%I:%M %p")

    slots = []
    current_time = start_time

    while current_time < end_time:
        if break_start <= current_time < break_end:
            current_time += timedelta(minutes=30)
            continue

        slots.append(current_time.strftime("%I:%M %p"))
        current_time += timedelta(minutes=30)

    return slots

# Request body model
class Appointment(BaseModel):
    name: str
    phone_number: str
    date: str
    time_slot: str

# API to fetch available slots
@app.get('/api/available_slots')
async def available_slots(date: str = Query(..., description="Date in YYYY-MM-DD format"), db: Session = Depends(get_db)):
    try:
        datetime.strptime(date, "%Y-%m-%d")  # Validate date format
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    booked_slots = db.query(AppointmentModel.time_slot).filter(AppointmentModel.date == date).all()
    booked_slots = [slot[0] for slot in booked_slots]
    all_slots = generate_slots()
    available_slots = [slot for slot in all_slots if slot not in booked_slots]

    return JSONResponse(content={"date": date, "available_slots": available_slots})

# Home route for render health check
@app.get("/")
async def root():
    return {"message": "Welcome to the Appointment Booking API!"}

# API to book an appointment
@app.post('/api/book_appointment')
async def book_appointment(appointment: Appointment, db: Session = Depends(get_db)):
    date = appointment.date
    time_slot = appointment.time_slot

    try:
        datetime.strptime(date, "%Y-%m-%d")  # Validate date format
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    all_slots = generate_slots()
    if time_slot not in all_slots:
        raise HTTPException(status_code=400, detail="Invalid time slot.")

    booked_slots = db.query(AppointmentModel.time_slot).filter(AppointmentModel.date == date).all()
    booked_slots = [slot[0] for slot in booked_slots]
    if time_slot in booked_slots:
        raise HTTPException(status_code=400, detail="Time slot already booked.")

    new_appointment = AppointmentModel(
        name=appointment.name,
        phone_number=appointment.phone_number,
        date=appointment.date,
        time_slot=appointment.time_slot
    )
    db.add(new_appointment)
    db.commit()

    return JSONResponse(content={"message": "Appointment booked successfully."}, status_code=201)
