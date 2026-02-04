from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit
# import cli_api_status

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

turnstiles = [
    {'id': 1, 'name': 'Tango01', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None },
    {'id': 2, 'name': 'Tango02', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None },
    {'id': 3, 'name': 'Tango03', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None },
    {'id': 4, 'name': 'Tango04', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None },
    {'id': 5, 'name': 'Tango05', 'status': 'locked', 'pistol': 'Off',  'codes': 0, 'code':None, 'code_response':None},
    {'id': 6, 'name': 'Tango06', 'status': 'locked', 'pistol': 'Off' , 'codes': 0, 'code':None, 'code_response':None},
    {'id': 7, 'name': 'Tango07', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None},
    {'id': 8, 'name': 'Tango08', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None},
    {'id': 9, 'name': 'Tango09', 'status': 'locked', 'pistol': 'Off',  'codes': 0, 'code':None, 'code_response':None},
    {'id': 10, 'name': 'Tango10', 'status': 'locked', 'pistol': 'Off','codes': 0, 'code':None, 'code_response':None},
    {'id': 11, 'name': 'Tango11', 'status': 'locked', 'pistol': 'Off','codes': 0, 'code':None, 'code_response':None},
    {'id': 12, 'name': 'Tango12', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None},
    {'id': 13, 'name': 'Tango13', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None},
    {'id': 14, 'name': 'Baliza-Proveedores', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None},
    {'id': 15, 'name': 'Tango15', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None},
    {'id': 16, 'name': 'Raspi16', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None},
    {'id': 17, 'name': 'Raspi17', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None},
    {'id': 18, 'name': 'Tango18', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None},
    {'id': 19, 'name': 'Tango19', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None},
    {'id': 20, 'name': 'Tango20', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None},
    {'id': 21, 'name': 'Baliza-Disca', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None},
    {'id': 22, 'name': 'Vehiculos', 'status': 'locked', 'pistol': 'Off', 'codes': 0, 'code':None, 'code_response':None}, 
]


def decode_turnstile_status(element):
    tsid = int(element[0].split('.')[3]) - 200
    turnstiles[tsid - 1]['status'] = element[1]


def decode_turnstile_pistol(element):
    tsid = int(element[0].split('.')[3]) - 200
    turnstiles[tsid - 1]['pistol'] = element[1]


def decode_turnstile_code(element):
    tsid = int(element[0].split('.')[3]) - 200
    code = element[1]
    code_response = element[2]
    turnstiles[tsid - 1]['codes'] += 1


@app.route('/')
def home():
    # Pass a variable to the HTML template
    return render_template('index.html', title='TURNSTILE MONITOR 2026', data=turnstiles)

@app.route('/fps')
def fps():
    # Pass a variable to the HTML template
    return turnstiles

@app.route('/api/hello', methods=['GET'])
def hello():
    name = request.args.get('name', default='World')
    ip = request.args.get('ip', default='localhost')
    print(f"hostname:{name} from IP:{ip}")
    print(ip)
    return jsonify({"message": f"Hello, {name} from IP:{ip}!"})

@app.route('/api/pistol', methods=['GET'])
def pistol():
    pistol = request.args.get('pistol', default='Off')
    ip = request.args.get('ip', default='localhost')
    decode_turnstile_pistol([ip, pistol])
    print(f"IP:{ip}, Pistol:{pistol}")
    return jsonify({"message": f"Pistol, {pistol} @ IP:{ip}!"})

@app.route('/api/status', methods=['GET'])
def status():
    status = request.args.get('status', default='locked')
    ip = request.args.get('ip', default='localhost')
    decode_turnstile_status([ip, status])
    print(f"IP:{ip}, STATUS:{status}")
    return jsonify({"message": f"Status, {status} @ IP:{ip}!"})

@app.route('/api/code', methods=['POST'])
def code():
    ip = request.args.get('ip', default='localhost')
    code = request.args.get('code', default='None')
    code_response = request.args.get('res', default='True')
    decode_turnstile_code([ip, code, code_response])
    return jsonify({"message": f"New Code @ IP:{ip}!"})

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

if __name__ == '__main__':
    socketio.run(app)