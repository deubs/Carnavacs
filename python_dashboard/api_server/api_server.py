from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit
import requests
import os
# import cli_api_status

CARNAVAL_API_URL = os.environ.get('CARNAVAL_API_URL', 'http://192.168.40.100')
API_TIMEOUT = 5

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

turnstiles = [
    {'id': 1, 'name': 'Tango01', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 2, 'name': 'Tango02', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 3, 'name': 'Tango03', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 4, 'name': 'Tango04', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 5, 'name': 'Tango05', 'status': 'locked', 'pistol': 'Off',  'codes': 0},
    {'id': 6, 'name': 'Tango06', 'status': 'locked', 'pistol': 'Off' , 'codes': 0},
    {'id': 7, 'name': 'Tango07', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 8, 'name': 'Tango08', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 9, 'name': 'Tango09', 'status': 'locked', 'pistol': 'Off',  'codes': 0},
    {'id': 10, 'name': 'Tango10', 'status': 'locked', 'pistol': 'Off','codes': 0},
    {'id': 11, 'name': 'Tango11', 'status': 'locked', 'pistol': 'Off','codes': 0},
    {'id': 12, 'name': 'Tango12', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 13, 'name': 'Tango13', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 14, 'name': 'Baliza-Proveedores', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 15, 'name': 'Tango15', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 16, 'name': 'Raspi16', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 17, 'name': 'Raspi17', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 18, 'name': 'Tango18', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 19, 'name': 'Tango19', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 20, 'name': 'Tango20', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 21, 'name': 'Baliza-Disca', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 22, 'name': 'Vehiculos', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
]

# C# API Helper Functions
def fetch_current_event():
    """GET /Events/Current"""
    try:
        resp = requests.get(f"{CARNAVAL_API_URL}/Events/Current", timeout=API_TIMEOUT)
        data = resp.json()
        return data.get('result') if data.get('success') else None
    except:
        return None

def fetch_event_stats():
    """GET /Events/Stats"""
    try:
        resp = requests.get(f"{CARNAVAL_API_URL}/Events/Stats", timeout=API_TIMEOUT)
        data = resp.json()
        return data.get('result') if data.get('success') else None
    except:
        return None

def fetch_gates():
    """GET /Gates/Gates"""
    try:
        resp = requests.get(f"{CARNAVAL_API_URL}/Gates/Gates", timeout=API_TIMEOUT)
        data = resp.json()
        return data.get('result', []) if data.get('success') else []
    except:
        return []

def fetch_devices():
    """GET /Gates/Devices"""
    try:
        resp = requests.get(f"{CARNAVAL_API_URL}/Gates/Devices", timeout=API_TIMEOUT)
        data = resp.json()
        return data.get('result', []) if data.get('success') else []
    except:
        return []

def decode_turnstile_status(element):
    tsid = int(element[0].split('.')[3]) - 200
    turnstiles[tsid - 1]['status'] = element[1]
    # cli_api_status.explore(turnstiles)
    # return home()

def decode_turnstile_pistol(element):
    tsid = int(element[0].split('.')[3]) - 200
    turnstiles[tsid - 1]['pistol'] = element[1]
    # return home()

def decode_turnstile_code(element):
    tsid = int(element[0].split('.')[3]) - 200
    turnstiles[tsid - 1]['codes'] += 1
    # return home()

@app.route('/')
def home():
    # Pass a variable to the HTML template
    return render_template('index.html', title='TURNSTILE MONITOR 2026', data=turnstiles)

@app.route('/fps')
def fps():
    # Pass a variable to the HTML template
    return turnstiles

@app.route('/dashboard-data')
def dashboard_data():
    # Fetch from C# API
    event = fetch_current_event()
    stats = fetch_event_stats()

    # Build device-to-peopleCount map from stats
    device_counts = {}
    if stats and stats.get('gates'):
        for gate in stats['gates']:
            for device in gate.get('accessDevices', []):
                device_counts[device['deviceName']] = {
                    'peopleCount': device['peopleCount'],
                    'gateName': gate['gateName'],
                    'gateNickName': device.get('gateNickName', '')
                }

    # Merge with local turnstile state
    merged = []
    for ts in turnstiles:
        api_data = device_counts.get(ts['name'], {})
        merged.append({
            'id': ts['id'],
            'name': ts['name'],
            'status': ts['status'],
            'pistol': ts['pistol'],
            'codes': api_data.get('peopleCount', 0),
            'gate': api_data.get('gateName', ''),
            'gateNickName': api_data.get('gateNickName', '')
        })

    return {
        'event': event,
        'stats': {
            'totalTickets': stats.get('totalTickets', 0) if stats else 0,
            'usedTickets': stats.get('usedTickets', 0) if stats else 0,
            'remainingTickets': stats.get('remainingTickets', 0) if stats else 0
        },
        'turnstiles': merged,
        'apiOnline': stats is not None
    }

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

@app.route('/api/code', methods=['GET'])
def code():
    ip = request.args.get('ip', default='localhost')
    decode_turnstile_code([ip, 'code'])
    return jsonify({"message": f"New Code @ IP:{ip}!"})

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

if __name__ == '__main__':
    socketio.run(app)