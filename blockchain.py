import os
import json
import time
import hashlib
import logging
from typing import List, Dict
from logging.handlers import RotatingFileHandler

# --- LOGGING SYSTEM INITIALIZATION ---
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "blockchain.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

handler = RotatingFileHandler(LOG_FILE, maxBytes=100000, backupCount=3, encoding="utf-8")

logging.basicConfig(
    handlers=[handler, logging.StreamHandler()],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("✅ Logging system initialized.")


# --- BLOCK CLASS ---
class Block:
    def __init__(self, index: int, previous_hash: str, transactions: List[Dict],
                 timestamp=None, nonce=0, hash=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = hash or self.calculate_hash()

    def calculate_hash(self) -> str:
        """Blok içeriğinden SHA-256 hash üretir."""
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty: int):
        """Proof-of-Work algoritması: hash'in başında difficulty kadar sıfır olmalı."""
        target = "0" * difficulty
        start_time = time.time()
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        elapsed = time.time() - start_time
        print(f"✅ Block mined: {self.hash}")
        print(f"⏱️ Mining completed in {elapsed:.2f} seconds.")
        logging.info(f"Block mined successfully. Hash: {self.hash}, Time: {elapsed:.2f}s")


# --- BLOCKCHAIN CLASS ---
class Blockchain:
    def __init__(self, difficulty=3, chain_file="chain.json"):
        self.difficulty = difficulty
        self.chain_file = chain_file
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict] = []
        self.mining_reward = 10
        self.load_chain()

    def create_genesis_block(self):
        """Zincirin ilk (genesis) bloğunu oluştur."""
        genesis_block = Block(0, "0", [], time.time())
        self.chain = [genesis_block]
        self.save_chain()
        logging.info("Genesis block created.")

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def create_transaction(self, sender: str, receiver: str, amount: float):
        """Yeni bir işlem oluştur ve bekleyen işlemlere ekle."""
        self.pending_transactions.append({
            "from": sender,
            "to": receiver,
            "amount": amount
        })
        logging.info(f"Transaction created: {sender} -> {receiver} ({amount})")

    def mine_pending_transactions(self, miner_address: str):
        """Bekleyen işlemleri yeni bir blokta birleştir ve madencilik yap."""
        if not self.pending_transactions:
            print("⚠️ No pending transactions to mine.")
            logging.warning("Attempted mining with no pending transactions.")
            return

        block = Block(len(self.chain), self.get_latest_block().hash, self.pending_transactions)
        block.mine_block(self.difficulty)

        self.chain.append(block)
        self.pending_transactions = [
            {"from": "SYSTEM", "to": miner_address, "amount": self.mining_reward}
        ]
        self.save_chain()

        logging.info(f"Block mined and added to chain. Index: {block.index}")

        if not self.is_chain_valid():
            logging.warning("Chain integrity might be compromised after mining!")

    def get_balance(self, address: str) -> float:
        """Bir adresin toplam bakiyesini döndür."""
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.get("from") == address:
                    balance -= tx.get("amount", 0)
                if tx.get("to") == address:
                    balance += tx.get("amount", 0)
        return balance

    def is_chain_valid(self) -> bool:
        """Zincirin bütünlüğünü kontrol et."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                print(f"❌ Hash mismatch at block {i}")
                return False
            if current.previous_hash != previous.hash:
                print(f"❌ Previous hash mismatch at block {i}")
                return False
        return True

    def save_chain(self):
        """Zinciri dosyaya kaydet."""
        try:
            with open(self.chain_file, "w") as f:
                json.dump([block.__dict__ for block in self.chain], f, indent=4)
            logging.info(f"Chain saved with {len(self.chain)} blocks.")
        except Exception as e:
            logging.error(f"Error saving chain: {e}")

    def load_chain(self):
        """Dosyadan zinciri yükle, yoksa genesis bloğunu oluştur."""
        try:
            with open(self.chain_file, "r") as f:
                data = json.load(f)
                self.chain = [Block(**block) for block in data]
                logging.info(f"Chain loaded successfully with {len(self.chain)} blocks.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("🌱 No existing chain found. Creating genesis block...")
            logging.warning("No existing chain found. Creating genesis block...")
            self.create_genesis_block()
