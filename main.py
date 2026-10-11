
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Healthcare Customer Service API")


# ============================================================
# USE CASE 1: APPOINTMENT MANAGEMENT
# ============================================================

appointments = {
    "APT45021": {
        "appointmentStatus": "CONFIRMED",
        "appointmentDate": "2026-10-12",
        "appointmentTime": "10:30 AM",
        "providerName": "Dr. Sharma",
        "appointmentType": "General Consultation",
        "rescheduleEligible": True,
        "cancellationEligible": True
    },
    "APT45022": {
        "appointmentStatus": "RESCHEDULED",
        "appointmentDate": "2026-10-15",
        "appointmentTime": "02:00 PM",
        "providerName": "Dr. Rao",
        "appointmentType": "Follow-up",
        "rescheduleEligible": True,
        "cancellationEligible": True
    },
    "APT45023": {
        "appointmentStatus": "CANCELLED",
        "appointmentDate": "2026-10-14",
        "appointmentTime": "09:00 AM",
        "providerName": "Dr. Mehta",
        "appointmentType": "Consultation",
        "rescheduleEligible": False,
        "cancellationEligible": False
    },
    "APT45024": {
        "appointmentStatus": "RESCHEDULE_NOT_ALLOWED",
        "appointmentDate": "2026-10-11",
        "appointmentTime": "11:15 AM",
        "providerName": "Dr. Iyer",
        "appointmentType": "Specialist Consultation",
        "rescheduleEligible": False,
        "cancellationEligible": False
    }
}


# ============================================================
# USE CASE 2: INSURANCE ELIGIBILITY
# ============================================================

insurance = {
    "INS784512": {
        "eligibilityStatus": "ACTIVE",
        "payerName": "ABC Health Insurance",
        "planName": "Standard Plus",
        "effectiveDate": "2026-01-01",
        "expirationDate": "2026-12-31",
        "verificationStatus": "VERIFIED"
    },
    "INS784513": {
        "eligibilityStatus": "INACTIVE",
        "payerName": "ABC Health Insurance",
        "planName": "Standard Plus",
        "effectiveDate": "2025-01-01",
        "expirationDate": "2025-12-31",
        "verificationStatus": "VERIFIED"
    },
    "INS784514": {
        "eligibilityStatus": "VERIFICATION_REQUIRED",
        "payerName": "ABC Health Insurance",
        "planName": "Basic Care",
        "effectiveDate": "2026-03-01",
        "expirationDate": "2027-02-28",
        "verificationStatus": "PENDING"
    },
    "INS784515": {
        "eligibilityStatus": "PAYER_MISMATCH",
        "payerName": "XYZ Insurance",
        "planName": "Premium Care",
        "effectiveDate": "2026-01-01",
        "expirationDate": "2026-12-31",
        "verificationStatus": "MISMATCH"
    }
}


# ============================================================
# USE CASE 3: LAB REPORT STATUS
# ============================================================

lab_reports = {
    "LAB90231": {
        "reportStatus": "PROCESSING",
        "testName": "Complete Blood Count",
        "collectionDate": "2026-10-07",
        "expectedAvailableDate": "2026-10-09",
        "reportAvailable": False,
        "deliveryMethod": "Patient Portal"
    },
    "LAB90232": {
        "reportStatus": "AVAILABLE",
        "testName": "Lipid Profile",
        "collectionDate": "2026-10-05",
        "expectedAvailableDate": "2026-10-07",
        "reportAvailable": True,
        "deliveryMethod": "Patient Portal"
    },
    "LAB90233": {
        "reportStatus": "DELAYED",
        "testName": "Thyroid Panel",
        "collectionDate": "2026-10-01",
        "expectedAvailableDate": "2026-10-05",
        "reportAvailable": False,
        "deliveryMethod": "Patient Portal"
    },
    "LAB90234": {
        "reportStatus": "ACCESS_ERROR",
        "testName": "Urine Analysis",
        "collectionDate": "2026-10-06",
        "expectedAvailableDate": "2026-10-08",
        "reportAvailable": False,
        "deliveryMethod": "Patient Portal"
    }
}


# ============================================================
# HOME ENDPOINT
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Healthcare Customer Service API is running"
    }


# ============================================================
# APPOINTMENT LOOKUP LOGIC
# ============================================================

def get_appointment_details(appointmentId: str):
    appointment_id = appointmentId.strip().upper()

    if appointment_id == "APT50000":
        raise HTTPException(
            status_code=500,
            detail="Simulated appointment backend failure"
        )

    record = appointments.get(appointment_id)

    if record is None:
        return {
            "appointmentId": appointment_id,
            "appointmentStatus": "NOT_FOUND",
            "message": "Appointment not found"
        }

    return {
        "appointmentId": appointment_id,
        **record
    }


# Original URL: /appointments/APT45021
@app.get("/appointments/{appointmentId}")
def appointment_by_path(appointmentId: str):
    return get_appointment_details(appointmentId)


# Fixed URL: /appointment-lookup?appointmentId=APT45021
@app.get("/appointment-lookup")
def appointment_lookup(
    appointmentId: str = Query(...)
):
    return get_appointment_details(appointmentId)


# ============================================================
# INSURANCE ENDPOINT
# ============================================================

@app.get("/insurance/{memberId}")
def get_insurance_eligibility(memberId: str):
    member_id = memberId.strip().upper()

    if member_id == "INS500000":
        raise HTTPException(
            status_code=500,
            detail="Simulated insurance backend failure"
        )

    record = insurance.get(member_id)

    if record is None:
        return {
            "memberId": member_id,
            "eligibilityStatus": "NOT_FOUND",
            "message": "Insurance member not found"
        }

    return {
        "memberId": member_id,
        **record
    }


# ============================================================
# LAB REPORT LOOKUP LOGIC
# ============================================================

def get_lab_report_status(reportId: str):
    report_id = reportId.strip().upper()

    if report_id == "LAB50000":
        raise HTTPException(
            status_code=500,
            detail="Simulated lab report backend failure"
        )

    record = lab_reports.get(report_id)

    if record is None:
        return {
            "reportId": report_id,
            "reportStatus": "NOT_FOUND",
            "message": "Lab report not found"
        }

    return {
        "reportId": report_id,
        **record
    }


# Original URL: /lab-reports/LAB90231
@app.get("/lab-reports/{reportId}")
def lab_report_by_path(reportId: str):
    return get_lab_report_status(reportId)


# Fixed URL: /lab-report-lookup?reportId=LAB90231
@app.get("/lab-report-lookup")
def lab_report_lookup(
    reportId: str = Query(...)
):
    return get_lab_report_status(reportId)
