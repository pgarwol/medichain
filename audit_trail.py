from dataclasses import dataclass
from datetime import datetime


@dataclass
class AuditTrail:
    id: str
    timestamp: datetime
    patient_id: str
    doctor_id: str
    # AccessType possibly?

    def __init__(self, patient_id: str, doctor_id: str):
        self.timestamp = datetime.now()
        print(self.timestamp)
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.id = self.generate_id()

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "audit_id": self.id,
            "timestamp": self.timestamp.isoformat()
        }

    def generate_id(self):
        audit_id = f"{self.patient_id}-{self.doctor_id}-{self.timestamp}"
        return audit_id.replace(" ", "")
