import hashlib
import json
from time import time
from typing import List


class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[dict], previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def proof_of_work(self, difficulty):
        print(f"Mining block {self.index}")
        self.nonce = 0
        computed_hash = self.compute_hash()
        while not computed_hash.startswith('0' * difficulty):
            self.nonce += 1
            computed_hash = self.compute_hash()
        print(f"Block {self.index} mined with hash: {computed_hash}")
        return computed_hash


class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.chain = []
        self.difficulty = difficulty  # Difficulty level for PoW
        self.pending_transactions = []  # Transactions waiting to be added to the blockchain
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time(), [], "0")
        genesis_block.hash = genesis_block.proof_of_work(self.difficulty)
        self.chain.append(genesis_block)

    def create_new_block_from_pending_transactions(self):
        if not self.pending_transactions:
            return False

        block = Block(
            index=len(self.chain),
            timestamp=time(),
            transactions=self.pending_transactions,
            previous_hash=self.chain[-1].hash
        )
        block.hash = block.proof_of_work(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []
        return True

    def add_transaction(self, transaction: dict):
        self.pending_transactions.append(transaction)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.compute_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True

    def mine_pending_transactions(self):
        mined = False
        while self.pending_transactions:
            mined = self.create_new_block_from_pending_transactions()
        return mined
