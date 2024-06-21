import base64
import os
import random

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class KeyManager:
    def __init__(self):
        self.doctor_keys = {}
        self.doctor_passwords = {}
        self.patient_codes = {}

    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def create_account(self, doctor_id_num: str, password: str):
        if doctor_id_num not in self.doctor_passwords:
            self.doctor_passwords[doctor_id_num] = {}
        salt = os.urandom(16)
        self.doctor_passwords[doctor_id_num]['salt'] = salt

        derived_key = self._derive_key(password, salt)
        enc_password = Fernet(derived_key).encrypt(password.encode())
        self.doctor_passwords[doctor_id_num]['password'] = enc_password

    def add_key(self, doctor_id_num: str, patient_id: str, key: str, password: str) -> int:
        if doctor_id_num not in self.doctor_passwords:
            raise ValueError("Password not set for the doctor.")

        salt = self.doctor_passwords[doctor_id_num]['salt']
        derived_key = self._derive_key(password, salt)
        cipher_suite = Fernet(derived_key)
        # print password
        if cipher_suite.decrypt(self.doctor_passwords[doctor_id_num]['password']).decode() != password:
            raise ValueError("Invalid password.")

        if doctor_id_num not in self.doctor_keys:
            self.doctor_keys[doctor_id_num] = {}

        encrypted_key = cipher_suite.encrypt(key.encode()).decode()
        self.doctor_keys[doctor_id_num][patient_id] = encrypted_key

        return self.generate_patient_code(patient_id, key)

    def get_key_from_password(self, doctor_id_num: str, patient_id: str, password: str):
        salt = self.doctor_passwords[doctor_id_num]['salt']
        if not salt:
            raise ValueError("Password not set for the doctor.")

        derived_key = self._derive_key(password, salt)
        cipher_suite = Fernet(derived_key)

        encrypted_key = self.doctor_keys[doctor_id_num].get(patient_id)
        if not encrypted_key:
            raise ValueError("No key found for the given patient ID.")

        try:
            decrypted_key = cipher_suite.decrypt(encrypted_key.encode()).decode()
            return decrypted_key
        except InvalidToken:
            raise ValueError("Invalid password.")

    def generate_patient_code(self, patient_id: str, key: str) -> int:
        if patient_id not in self.patient_codes:
            self.patient_codes[patient_id] = {}
        code = random.randint(1000000000, 9999999999)
        salt = os.urandom(16)
        self.patient_codes[patient_id]['salt'] = salt
        derived_key = self._derive_key(str(code), salt)
        enc_key = Fernet(derived_key).encrypt(key.encode())
        self.patient_codes[patient_id]['key'] = enc_key
        return code

    def get_key_from_code(self, patient_id: str, code: str) -> str:
        salt = self.patient_codes[patient_id]['salt']
        if not salt:
            raise ValueError("Code not set for the patient.")

        derived_key = self._derive_key(code, salt)
        cipher_suite = Fernet(derived_key)

        encrypted_key = self.patient_codes[patient_id]['key']
        try:
            decrypted_key = cipher_suite.decrypt(encrypted_key).decode()
            self.patient_codes.pop(patient_id)
            return decrypted_key
        except InvalidToken:
            raise ValueError("Invalid code.")


