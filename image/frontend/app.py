from flask import Flask, request, render_template, session
import requests
import time
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

@app.route('/')
def index():
    # Retrieve previous session values if they exist
    previous_data_size = session.get('data_size', '')
    previous_status_code = session.get('status_code', '')
    previous_destination_ip = session.get('destination_ip', '')
    message = session.get('message', '')

    return render_template('index.html', 
                           previous_data_size=previous_data_size, 
                           previous_status_code=previous_status_code, 
                           previous_destination_ip=previous_destination_ip,
                           message=message)

@app.route('/trigger', methods=['POST'])
def trigger():
    destination_ip = request.form['destination_ip']
    data_size = int(request.form['data_size']) * 1024 * 1024  # Convert MB to bytes
    status_code = request.form['status_code']
    data = 'x' * data_size
    payload = {
        'data': data,
        'status_code': status_code
    }
    
    start_time = time.time()
    response = requests.post(f'http://{destination_ip}:5002/receive', json=payload)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    message = f"{response.text} | Time taken: {elapsed_time:.8f} seconds"
    
    # Store the current input values in the session
    session['data_size'] = request.form['data_size']
    session['status_code'] = request.form['status_code']
    session['destination_ip'] = request.form['destination_ip']
    session['message'] = message
    
    return render_template('index.html', 
                           previous_data_size=request.form['data_size'], 
                           previous_status_code=request.form['status_code'], 
                           previous_destination_ip=request.form['destination_ip'],
                           message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)