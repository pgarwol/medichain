from dataclasses import dataclass
from datetime import datetime

from audit_trail import AuditTrail
from blockchain import Blockchain
from medical_data import MedicalHistory, MedicalRecord, Medication, Prescription


@dataclass
class AccessControl:
    read: tuple[str, ...]
    write: tuple[str, ...]
    edit: tuple[str, ...]

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
    blockchain: Blockchain

    def __init__(
            self,
            patient_id: str,
            doctor_id: str,
            read: tuple[str, ...],
            write: tuple[str, ...],
            edit: tuple[str, ...],
            blockchain: Blockchain
    ):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.access_control = AccessControl(read=read, write=write, edit=edit)
        self.medical_history = MedicalHistory()
        self.blockchain = blockchain

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
            # Create MedicalRecord
            medications = [Medication(name=p[0], amount=p[1]) for p in predicaments]
            prescription = Prescription(medications=tuple(medications))
            medical_record = MedicalRecord(prescription=prescription, note=comment, patient_id=patient_id)

            # Encrypt data
            encrypted_data = self.blockchain.encrypt_data(medical_record.__dict__, patient_id)
            audit_trail = AuditTrail(patient_id=patient_id, doctor_id=self.doctor_id)

            # Create transaction and mine block
            transaction = {
                "medical_data": encrypted_data,
                "audit_trail": audit_trail
            }
            self.blockchain.add_new_transaction(transaction)
            mined_block = self.blockchain.mine()

            return mined_block
        else:
            raise PermissionError("Doctor does not have write access to add medical records.")
