import hashlib
import json
import time
from typing import List, Dict


class Block:
    def __init__(self, index: int, previous_hash: str, transactions: List[Dict], timestamp=None, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty: int):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"✅ Block mined: {self.hash}")


class Blockchain:
    def __init__(self, difficulty=3, chain_file="chain.json"):
        self.difficulty = difficulty
        self.chain_file = chain_file
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict] = []
        self.mining_reward = 10
        self.load_chain()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", [], time.time())
        self.chain = [genesis_block]
        self.save_chain()

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def create_transaction(self, sender: str, receiver: str, amount: float):
        self.pending_transactions.append({
            "from": sender,
            "to": receiver,
            "amount": amount
        })

    def mine_pending_transactions(self, miner_address: str):
        block = Block(len(self.chain), self.get_latest_block().hash, self.pending_transactions)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = [
            {"from": "SYSTEM", "to": miner_address, "amount": self.mining_reward}
        ]
        self.save_chain()

    def get_balance(self, address: str) -> float:
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.get("from") == address:
                    balance -= tx.get("amount", 0)
                if tx.get("to") == address:
                    balance += tx.get("amount", 0)
        return balance

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                print("❌ Hash mismatch at block", i)
                return False
            if current.previous_hash != previous.hash:
                print("❌ Previous hash mismatch at block", i)
                return False
        return True

    def save_chain(self):
        with open(self.chain_file, "w") as f:
            json.dump([block.__dict__ for block in self.chain], f, indent=4)

    def load_chain(self):
        try:
            with open(self.chain_file, "r") as f:
                data = json.load(f)
                self.chain = [Block(**block) for block in data]
        except (FileNotFoundError, json.JSONDecodeError):
            print("🌱 No existing chain found. Creating genesis block...")
            self.create_genesis_block()
print(f"💾 Chain saved successfully with {len(self.chain)} blocks.")
