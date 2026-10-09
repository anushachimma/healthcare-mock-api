from fastapi import FastAPI, HTTPException

app = FastAPI(title="Healthcare Customer Service API")


# =====================================================================
# CHANGE 1 (UPDATED): Appointment data
# Before: only APT45021 existed.
# Now: one ID per status so every test case TC01-TC04 can be tested.
# =====================================================================
appointments = {
    # TC01 - CONFIRMED
    "APT45021": {
        "appointmentStatus": "CONFIRMED",
        "appointmentDate": "2026-10-12",
        "appointmentTime": "10:30 AM",
        "providerName": "Dr. Sharma",
        "appointmentType": "General Consultation",
        "rescheduleEligible": True,
        "cancellationEligible": True
    },
    # RESCHEDULED
    "APT45022": {
        "appointmentStatus": "RESCHEDULED",
        "appointmentDate": "2026-10-15",
        "appointmentTime": "02:00 PM",
        "providerName": "Dr. Rao",
        "appointmentType": "Follow-up",
        "rescheduleEligible": True,
        "cancellationEligible": True
    },
    # CANCELLED
    "APT45023": {
        "appointmentStatus": "CANCELLED",
        "appointmentDate": "2026-10-14",
        "appointmentTime": "09:00 AM",
        "providerName": "Dr. Mehta",
        "appointmentType": "Consultation",
        "rescheduleEligible": False,
        "cancellationEligible": False
    },
    # TC03 - RESCHEDULE_NOT_ALLOWED (restriction -> agent transfer)
    "APT45024": {
        "appointmentStatus": "RESCHEDULE_NOT_ALLOWED",
        "appointmentDate": "2026-10-11",
        "appointmentTime": "11:15 AM",
        "providerName": "Dr. Iyer",
        "appointmentType": "Specialist Consultation",
        "rescheduleEligible": False,
        "cancellationEligible": False
    },
}


# =====================================================================
# CHANGE 2 (NEW): Insurance data  (Use Case 2)
# =====================================================================
insurance = {
    # TC05 - ACTIVE + VERIFIED
    "INS784512": {
        "eligibilityStatus": "ACTIVE",
        "payerName": "ABC Health Insurance",
        "planName": "Standard Plus",
        "effectiveDate": "2026-01-01",
        "expirationDate": "2026-12-31",
        "verificationStatus": "VERIFIED"
    },
    # TC06 - INACTIVE
    "INS784513": {
        "eligibilityStatus": "INACTIVE",
        "payerName": "ABC Health Insurance",
        "planName": "Standard Plus",
        "effectiveDate": "2025-01-01",
        "expirationDate": "2025-12-31",
        "verificationStatus": "VERIFIED"
    },
    # TC07 - VERIFICATION_REQUIRED
    "INS784514": {
        "eligibilityStatus": "VERIFICATION_REQUIRED",
        "payerName": "ABC Health Insurance",
        "planName": "Basic Care",
        "effectiveDate": "2026-03-01",
        "expirationDate": "2027-02-28",
        "verificationStatus": "PENDING"
    },
    # PAYER_MISMATCH
    "INS784515": {
        "eligibilityStatus": "PAYER_MISMATCH",
        "payerName": "XYZ Insurance",
        "planName": "Premium Care",
        "effectiveDate": "2026-01-01",
        "expirationDate": "2026-12-31",
        "verificationStatus": "MISMATCH"
    },
}


# =====================================================================
# CHANGE 3 (NEW): Lab report data  (Use Case 3)
# =====================================================================
lab_reports = {
    # TC08 - PROCESSING
    "LAB90231": {
        "reportStatus": "PROCESSING",
        "testName": "Complete Blood Count",
        "collectionDate": "2026-10-07",
        "expectedAvailableDate": "2026-10-09",
        "reportAvailable": False,
        "deliveryMethod": "Patient Portal"
    },
    # TC09 - AVAILABLE
    "LAB90232": {
        "reportStatus": "AVAILABLE",
        "testName": "Lipid Profile",
        "collectionDate": "2026-10-05",
        "expectedAvailableDate": "2026-10-07",
        "reportAvailable": True,
        "deliveryMethod": "Patient Portal"
    },
    # TC10 - DELAYED
    "LAB90233": {
        "reportStatus": "DELAYED",
        "testName": "Thyroid Panel",
        "collectionDate": "2026-10-01",
        "expectedAvailableDate": "2026-10-05",
        "reportAvailable": False,
        "deliveryMethod": "Patient Portal"
    },
    # ACCESS_ERROR
    "LAB90234": {
        "reportStatus": "ACCESS_ERROR",
        "testName": "Urine Analysis",
        "collectionDate": "2026-10-06",
        "expectedAvailableDate": "2026-10-08",
        "reportAvailable": False,
        "deliveryMethod": "Patient Portal"
    },
}


@app.get("/")
def home():
    return {"message": "Healthcare Customer Service API is running"}


# ---------------------------------------------------------------------
# Use Case 1: Appointment  (UNCHANGED logic, plus test-error ID)
# ---------------------------------------------------------------------
@app.get("/appointments/{appointmentId}")
def get_appointment_details(appointmentId: str):
    # CHANGE 4 (NEW): simulate backend failure for error-handling test
    if appointmentId.upper() == "APT50000":
        raise HTTPException(status_code=500, detail="Internal server error")

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


# ---------------------------------------------------------------------
# CHANGE 5 (NEW): Use Case 2 endpoint
# ---------------------------------------------------------------------
@app.get("/insurance/{memberId}")
def get_insurance_eligibility(memberId: str):
    if memberId.upper() == "INS500000":
        raise HTTPException(status_code=500, detail="Internal server error")

    record = insurance.get(memberId.upper())

    if record is None:
        return {
            "eligibilityStatus": "NOT_FOUND",
            "memberId": memberId,
            "message": "Member not found"
        }

    return {
        "memberId": memberId.upper(),
        **record
    }


# ---------------------------------------------------------------------
# CHANGE 6 (NEW): Use Case 3 endpoint
# ---------------------------------------------------------------------
@app.get("/lab-reports/{reportId}")
def get_lab_report_status(reportId: str):
    if reportId.upper() == "LAB50000":
        raise HTTPException(status_code=500, detail="Internal server error")

    report = lab_reports.get(reportId.upper())

    if report is None:
        return {
            "reportStatus": "NOT_FOUND",
            "reportId": reportId,
            "message": "Report not found"
        }

    return {
        "reportId": reportId.upper(),
        **report
    }