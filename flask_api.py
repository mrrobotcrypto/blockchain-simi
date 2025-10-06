from flask import Flask, jsonify, request
from blockchain import Blockchain

# Flask uygulamasını başlat
app = Flask(__name__)

# Blockchain örneği oluştur
blockchain = Blockchain(difficulty=3)

# Ana endpoint
@app.route('/')

@app.route('/chain', methods=['GET'])
def get_chain():
    """Tüm blok zincirini JSON olarak döndürür."""
    chain_data = [block.__dict__ for block in blockchain.chain]
    response = {
        "length": len(chain_data),
        "chain": chain_data
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """Yeni bir işlem oluşturur."""
    values = request.get_json()

    # Gerekli alanlar
    required = ['from', 'to', 'amount']
    if not values:
        return jsonify({"error": "Missing JSON body"}), 400

    if not all(k in values for k in required):
        return jsonify({"error": "Missing fields in transaction"}), 400


if not isinstance(values['amount'], (int, float)) or values['amount'] <= 0:
    return jsonify({"error": "Amount must be a positive number"}), 400


    # İşlemi zincire ekle
    blockchain.create_transaction(values['from'], values['to'], values['amount'])
logging.info(f"API: New transaction added from {values['from']} to {values['to']} amount {values['amount']}")




    response = {
        "message": "Transaction added successfully",
        "transaction": values
    }
    return jsonify(response), 201




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
