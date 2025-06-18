from flask import Flask, send_file, request, jsonify
from interfaceFacade import GerenciamentoDeCarteiras
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
gerenciador = GerenciamentoDeCarteiras()

@app.route("/api/carteiras", methods=["GET"])
def listar_carteiras():
    """
    Rota GET que retorna todas as carteiras.
    """
    carteiras = gerenciador.get_carteiras()
    return jsonify(carteiras)  

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


@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    try:
        return send_file('../data.json', mimetype='application/json')
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)