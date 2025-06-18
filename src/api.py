from flask import Flask, jsonify, request
from flask_cors import CORS
from interfaceFacade import GerenciamentoDeCarteiras

app = Flask(__name__)
CORS(app)

# Create a single instance of GerenciamentoDeCarteiras
gerenciador = GerenciamentoDeCarteiras()

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    try:
        # Get transactions from storage through gerenciador
        transactions = gerenciador.get_transacoes()
        
        # Convert to dict with explicit checking
        if not transactions:
            return jsonify([])
            
        transactions_dict = [t.to_dict() for t in transactions]
    
        
        response = jsonify(transactions_dict)
        
        return response
    except Exception as e:
        print("Error in API:", str(e))
        return {'error': str(e)}, 500

@app.route('/api/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    try:
        updated_data = request.json
        
        # Find the original transaction
        original_transaction = next(
            t for t in gerenciador.get_transacoes() 
            if t.id == transaction_id
        )
        
        # Update the transaction using the facade
        success, message = gerenciador.editar_transacao(
            original_transaction,
            updated_data
        )
        
        if not success:
            return {'error': message}, 400
            
        return jsonify({'message': message})
        
    except StopIteration:
        return {'error': 'Transaction not found'}, 404
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)