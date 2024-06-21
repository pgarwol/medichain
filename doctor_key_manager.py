import json
import base64
import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class DoctorKeyManager:
    def __init__(self):
        self.keys = {}  # {doctor_id: {patient_id: encrypted_key}}
        self.salts = {}  # {doctor_id: salt}
        self.passwords = {}  # {doctor_id: password}

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
        salt = os.urandom(16)
        self.salts[doctor_id_num] = salt

        derived_key = self._derive_key(password, salt)
        enc_password = Fernet(derived_key).encrypt(password.encode())
        self.passwords[doctor_id_num] = enc_password

    def add_key(self, doctor_id_num: str, patient_id: str, key: str, password: str):
        if doctor_id_num not in self.salts:
            raise ValueError("Password not set for the doctor.")

        salt = self.salts[doctor_id_num]
        derived_key = self._derive_key(password, salt)
        cipher_suite = Fernet(derived_key)
        # print password
        if cipher_suite.decrypt(self.passwords[doctor_id_num]).decode() != password:
            raise ValueError("Invalid password.")

        if doctor_id_num not in self.keys:
            self.keys[doctor_id_num] = {}

        encrypted_key = cipher_suite.encrypt(key.encode()).decode()
        self.keys[doctor_id_num][patient_id] = encrypted_key

    def get_key(self, doctor_id_num: str, patient_id: str, password: str):
        salt = self.salts.get(doctor_id_num)
        if not salt:
            raise ValueError("Password not set for the doctor.")

        derived_key = self._derive_key(password, salt)
        cipher_suite = Fernet(derived_key)

        encrypted_key = self.keys[doctor_id_num].get(patient_id)
        if not encrypted_key:
            raise ValueError("No key found for the given patient ID.")

        try:
            decrypted_key = cipher_suite.decrypt(encrypted_key.encode()).decode()
            return decrypted_key
        except InvalidToken:
            raise ValueError("Invalid password.")
