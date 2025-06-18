# =========================================
# Módulo: api.py
# Descrição: API Flask para gerenciamento de carteiras, cofrinhos e transações.
# =========================================
import json
import sys
from pathlib import Path

# src directory pro Python path
src_path = str(Path(__file__).resolve().parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)
    
from flask import Flask, jsonify, request, request, jsonify
from facade.gerenciadorCarteiras import GerenciamentoDeCarteiras
from flask_cors import CORS
from facade.gerenciadorCarteiras import GerenciamentoDeCarteiras
from core.transacao import Receita

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
gerenciador = GerenciamentoDeCarteiras()

@app.route("/api/carteiras", methods=["GET"])
def listar_carteiras():
    """
    Retorna a lista de carteiras cadastradas no sistema.
    """
    carteiras = gerenciador.get_carteiras()
    carteiras_dict = [c.to_dict() for c in carteiras]
    return jsonify(carteiras_dict)  

@app.route("/api/carteiras", methods=["POST"])
def criar_carteira():
    """
    Cria uma nova carteira a partir dos dados enviados no corpo da requisição.
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
    """
    Retorna a lista de cofrinhos cadastrados no sistema.
    """
    cofrinhos = gerenciador.get_cofrinhos() 
    cofrinhos_dict = [c.to_dict() for c in cofrinhos]
    return jsonify(cofrinhos_dict)


@app.route("/api/cofrinhos", methods=["POST"])
def criar_cofrinho():
    """
    Cria um novo cofrinho a partir dos dados enviados no corpo da requisição.
    """
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
    """
    Realiza um depósito de uma carteira para um cofrinho.
    """
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
    """
    Quebra um cofrinho, transferindo o saldo para uma carteira de destino.
    """
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
    """
    Retorna as categorias disponíveis para transações.
    """
    categorias = gerenciador.get_categorias_disponiveis()
    return jsonify(categorias)

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """
    Retorna todas as transações cadastradas no sistema.
    """
    try:
        
        transactions = gerenciador.get_transacoes()
        
        if not transactions:
            return jsonify([])
            
        transactions_dict = [t.to_dict() for t in transactions]
    
        
        response = jsonify(transactions_dict)
        
        return response
    except Exception as e:
        print("Error in API:", str(e))
        return {'error': str(e)}, 500

@app.route('/api/transactions/monthly-totals/<string:month>', methods=['GET'])
def get_monthly_totals(month):
    """
    Retorna o total de receitas, despesas e saldo para um mês específico.
    """
    try:
        transactions = gerenciador.get_transacoes()
        
        month_transactions = [
            t for t in transactions 
            if t.data.startswith(month)
        ]
        for c in month_transactions:
            print(c.data)
        
        total_receitas = sum(t._valor for t in month_transactions if isinstance(t, Receita))
        total_despesas = sum(t._valor for t in month_transactions if not isinstance(t, Receita))
        saldo = total_receitas - total_despesas
        return jsonify({
            'receitas': total_receitas,
            'despesas': total_despesas,
            'saldo': saldo
        })
        
    except Exception as e:
        print("Error calculating monthly totals:", str(e))
        return {'error': str(e)}, 500

@app.route('/api/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    """
    Atualiza uma transação existente com os dados fornecidos.
    """
    try:
        updated_data = request.json
        
        
        original_transaction = next(
            t for t in gerenciador.get_transacoes() 
            if t.id == transaction_id
        )
        
        
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
    """
    Deleta uma transação pelo seu ID.
    """
    try:
        
        transaction = next(
            t for t in gerenciador.get_transacoes() 
            if t.id == transaction_id
        )
        
        
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
    """
    Cria uma nova transação (receita ou despesa) a partir dos dados enviados no corpo da requisição.
    """
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

        
        try:
            if data.get('receita'):
                print("woooo")
                success, message = gerenciador.adicionar_receita(
                    nome=data['nome'],
                    valor=valor,
                    tipo=data['categoria'],  
                    data=data['data'],
                    desc=data['desc'],
                    carteira=carteira,
                    rep=data['repeticao']
                )
            else:
                success, message = gerenciador.adicionar_despesa(
                    nome=data['nome'],
                    valor=valor,
                    tipo=data['categoria'], 
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

@app.route("/api/pontos", methods=["GET"])
def get_pontos_usuario():
    """
    Retorna os pontos do usuário, metas e gastos do sistema de pontos.
    """
    sistema = gerenciador.get_pontos() 
    data = {
        "pontos": sistema.get_pontos(),
        **sistema.get_metas(),
        **sistema.get_gastos()
    }
    return jsonify({"pontos": data})

@app.route('/api/carteiras/<string:carteira_nome>', methods=['DELETE'])
def deletar_carteira(carteira_nome):
    """
    Deleta uma carteira pelo nome, se ela existir e estiver com saldo zero.
    """
    try:
        carteiras = gerenciador.get_carteiras()
        carteira = next((c for c in carteiras if c.get_nome() == carteira_nome), None)
        if not carteira:
            return jsonify({'success': False, 'message': 'Carteira não encontrada.'}), 404
        success, message = gerenciador.deletar_carteira(carteira)
        if not success:
            return jsonify({'success': False, 'message': message}), 400
        return jsonify({'success': True, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)