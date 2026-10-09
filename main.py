
from fastapi import FastAPI

app = FastAPI(title="Healthcare Customer Service API")


# Mock appointment data for assignment testing
appointments = {
    "APT45021": {
        "appointmentStatus": "CONFIRMED",
        "appointmentDate": "2026-10-12",
        "appointmentTime": "10:30 AM",
        "providerName": "Dr. Sharma",
        "appointmentType": "General Consultation",
        "rescheduleEligible": True,
        "cancellationEligible": True
    }
}


@app.get("/")
def home():
    return {"message": "Healthcare Customer Service API is running"}


@app.get("/appointments/{appointmentId}")
def get_appointment_details(appointmentId: str):
    appointment = appointments.get(appointmentId.upper())

    if appointment is None:
        return {
            "appointmentStatus": "NOT_FOUND",
            "appointmentId": appointmentId,
            "message": "Appointment not found"
        }

    return {
        "appointmentId": appointmentId.upper(),
        **appointment
    }