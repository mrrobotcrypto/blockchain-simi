
print("🚀 Starting blockchain simulation...\n")

from blockchain import Blockchain

chain = Blockchain(difficulty=3)

chain.create_transaction("Alice", "Bob", 20)
chain.create_transaction("Bob", "Charlie", 5)

print("⛏️ Mining pending transactions...")
chain.mine_pending_transactions("Miner1")

print("\n--- Balances ---")
for name in ["Alice", "Bob", "Charlie", "Miner1"]:
    print(f"{name}: {chain.get_balance(name)}")

print("\nChain valid?", chain.is_chain_valid())


