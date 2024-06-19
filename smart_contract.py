from dataclasses import dataclass, field
from datetime import datetime

from medical_data import MedicalHistory, MedicalRecord, Medication, Prescription
from typing import Tuple


@dataclass
class AccessControl:
    read: Tuple[str]
    write: Tuple[str]
    edit: Tuple[str]

    def can_read(self, accessing_entity_id) -> bool:
        return accessing_entity_id in self.read

    def can_write(self, accessing_entity_id) -> bool:
        return accessing_entity_id in self.write

    def can_edit(self, accessing_entity_id) -> bool:
        return accessing_entity_id in self.edit


@dataclass
class SmartContract:
    patient_id: str
    doctor_id: str
    access_control: AccessControl
    medical_history: MedicalHistory

    def __init__(
            self,
            patient_id: str,
            doctor_id: str,
            read: Tuple[str],
            write: Tuple[str],
            edit: Tuple[str],
    ):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.access_control = AccessControl(read=read, write=write, edit=edit)
        self.medical_history = MedicalHistory()

    def handle_access(self, access_type: str):
        match access_type:
            case "read":
                pass
            case "write":
                pass
            case "edit":
                pass
            case _:
                print("Something went wrong.")

    def execute(self, func: callable):
        func()

    def add_medical_record(self, date: datetime, patient_id: str, comment: str, predicaments: list[tuple[str, int]]):
        if self.access_control.can_write(self.doctor_id):
            medications = [Medication(name=name, amount=amount) for name, amount in predicaments]
            prescription = Prescription(medications=tuple(medications))
            medical_record = MedicalRecord(prescription=prescription, note=comment, patient_id=patient_id)
            self.medical_history.write(medical_record)
            print(f"Medical record added for patient {patient_id} on {date}")
            return True
        else:
            print(f"Access denied for doctor {self.doctor_id} to add medical record")
            return False

