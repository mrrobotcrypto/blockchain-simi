from flask import Flask, jsonify, request
from blockchain import Blockchain

# Flask uygulamasını başlat
app = Flask(__name__)

# Blockchain örneği oluştur
blockchain = Blockchain(difficulty=3)

# Ana endpoint
@app.route('/')
def index():
    return jsonify({
        "message": "Welcome to the Blockchain API!",
        "endpoints": {
            "/chain": "Get the full blockchain",
            "/mine": "Mine new block with pending transactions",
            "/transactions/new": "Create a new transaction"
        }
    }), 200


# Uygulamayı başlat
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
