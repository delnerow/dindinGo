import json
from flask import Flask, jsonify, request, request, jsonify
from interfaceFacade import GerenciamentoDeCarteiras
from flask_cors import CORS
from interfaceFacade import GerenciamentoDeCarteiras

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
gerenciador = GerenciamentoDeCarteiras()

@app.route("/api/carteiras", methods=["GET"])
def listar_carteiras():
    carteiras = gerenciador.get_carteiras()
    carteiras_dict = [c.to_dict() for c in carteiras]
    return jsonify(carteiras_dict)  

@app.route("/api/carteiras", methods=["POST"])
def criar_carteira():
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
                "desc": desc,
                "saldo": saldo
            }
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": message
        }), 400

@app.route("/api/cofrinhos", methods=["GET"])
def listar_cofrinhos():
    cofrinhos = gerenciador.get_cofrinhos() 
    cofrinhos_dict = [c.to_dict() for c in cofrinhos]
    return jsonify(cofrinhos_dict)


@app.route("/api/cofrinhos", methods=["POST"])
def criar_cofrinho():
    data = request.get_json()
    nome = data.get("nome")
    desc = data.get("desc")
    timer_mes = int(data.get("timer_mes", 0))
    meta_valor = float(data.get("meta_valor", 0.0))
    saldo = float(data.get("saldo", 0.0))

    success, message = gerenciador.adicionar_cofrinho(nome, desc, timer_mes, meta_valor, saldo)

    if success:
        return jsonify({
            "success": True,
            "cofrinho": {
                "nome": nome,
                "desc": desc,
                "timer_mes": timer_mes,
                "saldo": saldo,
                "meta_valor": meta_valor
            }
        }), 200
    else:
        return jsonify({ "success": False, "message": message }), 400

@app.route("/api/cofrinhos/<string:cofrinho_nome>/depositar", methods=["POST"])
def fazer_deposito(cofrinho_nome):
    data = request.get_json()
    valor = float(data.get("valor", 0.0))
    carteira_nome = data.get("carteiras")
    print("Valor do depósito:", valor)

    cofrinhos = gerenciador.get_cofrinhos()
    cofrinho = next((c for c in cofrinhos if c.get_nome() == cofrinho_nome), None)
    print("Cofrinho encontrado:", cofrinho.get_nome())
    if not cofrinho:
        return jsonify({"success": False, "message": "Cofrinho não encontrado."}), 404


    carteiras = gerenciador.get_carteiras()
    carteira_origem = next((c for c in carteiras if c.get_nome() == carteira_nome), None)
    print("Carteira de origem encontrada:", carteira_origem.get_nome())
    if not carteira_origem:
        return jsonify({"success": False, "message": "Carteira de origem não encontrada."}), 404

    success, message = gerenciador.depositar_cofrinho(valor, cofrinho, carteira_origem)

    if success:
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "message": message}), 400

@app.route("/api/cofrinhos/<string:cofrinho_nome>/quebrar", methods=["POST"])
def quebrar_cofrinhos(cofrinho_nome):
    data = request.get_json()
    carteira_nome = data.get("carteira")
    print("Cofrinho encontrado:", cofrinho_nome)
    if not carteira_nome:
        return jsonify({"success": False, "message": "Carteira de destino não fornecida."}), 400

    cofrinhos = gerenciador.get_cofrinhos()
    cofrinho = next((c for c in cofrinhos if c.get_nome() == cofrinho_nome), None)
    if not cofrinho:
        return jsonify({"success": False, "message": "Cofrinho não encontrado."}), 404

    carteiras = gerenciador.get_carteiras()
    carteira_nome= next((c for c in carteiras if c.get_nome() == carteira_nome), None)
    if not carteira_nome:
        return jsonify({"success": False, "message": "Carteira de destino não encontrada."}), 404

    valor, msg = gerenciador.quebrar_cofrinho(cofrinho, carteira_nome)
    return jsonify({"success": True, "message": f"Cofrinho '{cofrinho_nome}' quebrado. R$ {valor:.2f} retornados."})

@app.route("/api/categorias", methods=["GET"])
def listar_categorias():
    categorias = gerenciador.get_categorias_disponiveis()
    return jsonify(categorias)

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
                    rep=data['repeticao']
                )
            else:
                success, message = gerenciador.adicionar_despesa(
                    nome=data['nome'],
                    valor=valor,
                    tipo=data['categoria'],  # Changed from categoria to tipo
                    data=data['data'],
                    desc=data['desc'],
                    carteira=carteira,
                    rep=data['repeticao']
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