from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/receive', methods=['POST'])
def receive():
    payload = request.get_json()
    data = payload.get('data', '')
    status_code = int(payload.get('status_code', 200))
    return Response(f'Received {len(data)} bytes of data', status=status_code), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)