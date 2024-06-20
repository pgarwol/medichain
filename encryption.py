import json
from typing import Any

from cryptography.fernet import Fernet, InvalidToken


class CryptographyHelper:
    def __init__(self, key: bytes = None):
        self.key = Fernet.generate_key() if key is None else key
        self.cipher_suite = Fernet(self.key)

    def encrypt_data(self, data: Any) -> str:
        serialized_data = str(data).encode()
        encrypted_data = self.cipher_suite.encrypt(serialized_data)
        return encrypted_data.decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        decrypted_data = self.cipher_suite.decrypt(encrypted_data.encode())
        return decrypted_data.decode()

    def get_key(self) -> str:
        return self.key.decode()


class CryptographyManager:
    def __init__(self):
        self.keys = {}  # Store keys for each item

    def encrypt_item(self, item_id: str, data: Any) -> str:
        helper = CryptographyHelper()
        data = json.dumps(data)
        encrypted_data = helper.encrypt_data(data)
        self.keys[item_id] = helper.get_key()
        return encrypted_data

    def decrypt_item(self, item_id: str, encrypted_data: str, provided_key: str) -> dict | None:
        key = self.keys.get(item_id)
        if not key:
            raise ValueError("No key found for the given item ID.")
        if provided_key != key:
            raise ValueError("Provided key does not match the stored key.")
        helper = CryptographyHelper(key=provided_key.encode())
        try:
            data = helper.decrypt_data(encrypted_data)
            return json.loads(data)
        except InvalidToken:
            return None

    def check_key(self, item_id: str, encrypted_data: str, provided_key: str) -> bool:
        try:
            helper = CryptographyHelper(key=provided_key.encode())
            helper.decrypt_data(encrypted_data)
            return True
        except InvalidToken:
            return False


if __name__ == "__main__":
    manager = CryptographyManager()

    item_id1 = "item1"
    original_data1 = "Hello, World!"
    encrypted_data1 = manager.encrypt_item(item_id1, original_data1)
    print(f"Encrypted data for {item_id1}: {encrypted_data1}")

    item_id2 = "item2"
    original_data2 = "Another message"
    encrypted_data2 = manager.encrypt_item(item_id2, original_data2)
    print(f"Encrypted data for {item_id2}: {encrypted_data2}")

    provided_key1 = manager.keys[item_id1]
    print(provided_key1)
    if manager.check_key(item_id1, encrypted_data1, provided_key1):
        decrypted_data1 = manager.decrypt_item(item_id1, encrypted_data1, provided_key1)
        print(f"Decrypted data for {item_id1}: {decrypted_data1}")
    else:
        print("Invalid key provided for item1")

    provided_key2 = manager.keys[item_id2]
    if manager.check_key(item_id2, encrypted_data2, provided_key2):
        decrypted_data2 = manager.decrypt_item(item_id2, encrypted_data2, provided_key2)
        print(f"Decrypted data for {item_id2}: {decrypted_data2}")
    else:
        print("Invalid key provided for item2")
