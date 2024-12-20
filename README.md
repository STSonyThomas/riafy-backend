# Appointment Booking API - README

## Overview
This project is a FastAPI-based application for managing appointment bookings. It allows users to view available time slots and book appointments while preventing double bookings.

---

## Requirements
- Python 3.8+
- SQLite (comes pre-installed with Python)

---

## Setup Instructions

### Step 1: Clone the Repository
```bash
# Clone the repository
git clone <repository_url>
cd <repository_directory>
```

### Step 2: Create a Virtual Environment
A virtual environment is recommended to isolate dependencies.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
Ensure you have `pip` installed and up to date. Install the required dependencies from `requirements.txt`.

```bash
# Install dependencies
pip install -r requirements.txt
```

### Step 4: Run the Application
Run the FastAPI application using `uvicorn`.

```bash
# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will be accessible at `http://127.0.0.1:8000`.

---

## API Endpoints

### 1. Fetch Available Slots
**Endpoint:** `GET /api/available_slots`

**Query Parameter:**
- `date` (required): Date in `YYYY-MM-DD` format.

**Response:**
```json
{
    "date": "2024-12-20",
    "available_slots": ["10:00 AM", "10:30 AM", ...]
}
```

### 2. Book an Appointment
**Endpoint:** `POST /api/book_appointment`

**Request Body:**
```json
{
    "name": "John Doe",
    "phone_number": "1234567890",
    "date": "2024-12-20",
    "time_slot": "10:00 AM"
}
```

**Response:**
```json
{
    "message": "Appointment booked successfully."
}
```

---

## Notes
- Ensure that the `date` is in `YYYY-MM-DD` format.
- Time slots from `1:00 PM` to `2:00 PM` are unavailable due to a break.
- Prevents double-booking of time slots.

---

## Additional Commands

### Deactivate the Virtual Environment
```bash
deactivate
```

---

## Troubleshooting
- If you encounter issues with dependencies, ensure your `pip` is up to date:
```bash
pip install --upgrade pip
```

