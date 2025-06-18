import json
from flask import Flask, jsonify, request, request, jsonify
from interfaceFacade import GerenciamentoDeCarteiras
from flask_cors import CORS
from interfaceFacade import GerenciamentoDeCarteiras

app = Flask(__name__)
CORS(app)
gerenciador = GerenciamentoDeCarteiras()

@app.route("/api/carteiras", methods=["GET"])
def listar_carteiras():
    """
    Rota GET que retorna todas as carteiras.
    """
    carteiras = gerenciador.get_carteiras()
    carteiras_dict = [c.to_dict() for c in carteiras]
    return jsonify(carteiras_dict)  

@app.route("/api/carteiras", methods=["POST"])
def criar_carteira():
    """
    Rota POST que cria uma nova carteira.
    Espera JSON com: nome, desc, saldo.
    """
    data = request.get_json()
    nome = data.get("nome")
    desc = data.get("desc")
    saldo = float(data.get("saldo", 0.0))

    success, message = gerenciador.adicionar_carteira(nome, desc, saldo)

    if success:
        return jsonify({
            "success": True,
            "carteira": {
                "nome": nome,
                "descricao": desc,
                "saldo": saldo
            }
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": message
        }), 400


# Create a single instance of GerenciamentoDeCarteiras

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

@app.route('/api/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        # Find the transaction to delete
        transaction = next(
            t for t in gerenciador.get_transacoes() 
            if t.id == transaction_id
        )
        
        # Delete the transaction using the facade
        success, message = gerenciador.deletar_transacao(transaction)
        
        if not success:
            return {'error': message}, 400
            
        return jsonify({'message': message})
        
    except StopIteration:
        return {'error': 'Transaction not found'}, 404
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    try:
        data = request.json
        print("\n=== Transaction Creation Debug ===")
        print("1. Received Data:", json.dumps(data, indent=2))

        try:
            valor = float(data['valor'])
            print("2. Converted valor:", valor)
        except (ValueError, TypeError) as e:
            print("Error converting valor:", str(e))
            return {'error': 'Valor inválido: deve ser um número'}, 400

        # Get the carteira object
        try:
            carteiras = gerenciador.get_carteiras()
            carteira = next(
                (c for c in carteiras if c.get_nome() == data['carteira']),
                None
            )
            print("4. Found carteira:", carteira)
        except Exception as e:
            print("Error finding carteira:", str(e))
            return {'error': f'Erro ao buscar carteira: {str(e)}'}, 400

        if not carteira:
            return {'error': f'Carteira não encontrada: {data["carteira"]}'}, 400

        # Call the correct facade methods with the right parameters
        try:
            if data.get('receita'):
                print("woooo")
                success, message = gerenciador.adicionar_receita(
                    nome=data['nome'],
                    valor=valor,
                    tipo=data['categoria'],  # Changed from categoria to tipo
                    data=data['data'],
                    desc=data['desc'],
                    carteira=carteira,
                    fixo=data['repeticao']
                )
            else:
                success, message = gerenciador.adicionar_despesa(
                    nome=data['nome'],
                    valor=valor,
                    tipo=data['categoria'],  # Changed from categoria to tipo
                    data=data['data'],
                    desc=data['desc'],
                    carteira=carteira,
                    fixo=data['repeticao']
                )

            if not success:
                return {'error': message}, 400

            return jsonify({'message': message}), 201

        except Exception as e:
            print("Error in transaction creation:", str(e))
            return {'error': str(e)}, 500

    except Exception as e:
        print("Error in request handling:", str(e))
        return {'error': str(e)}, 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)