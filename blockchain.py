import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any

from audit_trail import AuditTrail
from encryption import CryptographyManager


@dataclass
class Block:
    index: int
    timestamp: datetime
    medical_data: str
    audit_trail: AuditTrail
    previous_hash: str
    hash: str = ""

    def compute_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True, default=str)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict[str, Any]] = []
        self.create_genesis_block()
        self.cryptography_manager = CryptographyManager()

    def create_genesis_block(self):
        genesis_block = Block(
            index=0,
            timestamp=datetime.now(),
            medical_data="Genesis Block",
            audit_trail=AuditTrail(patient_id="0", doctor_id="0"),
            previous_hash="0"
        )
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_new_block(self, block: Block):
        block.previous_hash = self.get_last_block().hash
        block.hash = block.compute_hash()
        self.chain.append(block)

    def add_new_transaction(self, transaction: Dict[str, Any]):
        self.pending_transactions.append(transaction)

    def mine(self):
        if not self.pending_transactions:
            return False

        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            timestamp=datetime.now(),
            medical_data=self.pending_transactions[0]["medical_data"],
            audit_trail=self.pending_transactions[0]["audit_trail"],
            previous_hash=last_block.hash
        )
        new_block.hash = new_block.compute_hash()
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def encrypt_data(self, data: Any, item_id: str) -> str:
        return self.cryptography_manager.encrypt_item(item_id, data)

    def decrypt_data(self, encrypted_data: str, item_id: str, provided_key: str) -> str:
        return self.cryptography_manager.decrypt_item(item_id, encrypted_data, provided_key)
