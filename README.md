# 🧱 Blockchain-Sim

**Blockchain-Sim** is a lightweight, fully functional mini blockchain network built with **Python** and **Flask**.  
It simulates the essential mechanisms of a decentralized ledger — including **mining**, **transactions**, **balances**, and **node consensus**.

---

## 🚀 Features

✅ Peer Discovery – Nodes can register and list other peers in the network  
✅ Consensus Mechanism – Uses the *Longest Chain Rule* to resolve conflicts  
✅ Mining System – Proof-of-Work mining with automatic reward allocation  
✅ Transaction Handling – Add and validate pending transactions easily  
✅ Balance Query – Real-time wallet balance tracking for each address  
✅ Persistent Chain – Blockchain data saved to `chain.json`  
✅ RESTful API – Access blockchain data via `/chain` and related endpoints  
✅ Logging System – Tracks mining, transactions, and network activity  

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/chain` | Returns the full blockchain |
| `POST` | `/transactions/new` | Creates a new transaction |
| `GET` | `/mine` | Mines pending transactions |
| `GET` | `/balance/<address>` | Returns balance for a specific wallet |
| `POST` | `/nodes/register` | Registers new peer nodes |
| `GET` | `/nodes` | Lists all known nodes in the network |
| `GET` | `/nodes/resolve` | Resolves conflicts using consensus |

---

## ⚙️ Installation & Run

```bash
# Clone the repo
git clone https://github.com/mrrobotcrypto/blockchain-simi
cd blockchain-simi

# Install dependencies
pip install flask requests

# Run the main node (default port 5000)
python flask_api.py
