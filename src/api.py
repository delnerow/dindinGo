from flask import Flask, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    try:
        return send_file('../data.json', mimetype='application/json')
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)