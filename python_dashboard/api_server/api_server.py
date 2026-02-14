from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_socketio import SocketIO, emit
from functools import wraps
import requests
import os
from datetime import datetime
import threading
# import cli_api_status

keys = {'key1': 'ed5976ff-2a98-470a-b90e-bf945d25c5c9',
'key2': '840c53ea-0467-4b52-b083-2de869d939a8',
'key3': '2329db1e-95e8-4265-986e-d02114dbf5dc'}

CARNAVAL_API_URL = os.environ.get('CARNAVAL_API_URL', 'http://192.168.40.101')
API_TIMEOUT = 5

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'your_secret_key')
socketio = SocketIO(app)

turnstiles = [
    {'id': 1, 'name': 'tango01', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 2, 'name': 'tango02', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 3, 'name': 'tango03', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 4, 'name': 'tango04', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 5, 'name': 'tango05', 'status': 'locked', 'pistol': 'Off',  'codes': 0},
    {'id': 6, 'name': 'tango06', 'status': 'locked', 'pistol': 'Off' , 'codes': 0},
    {'id': 7, 'name': 'tango07', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 8, 'name': 'tango08', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 9, 'name': 'tango09', 'status': 'locked', 'pistol': 'Off',  'codes': 0},
    {'id': 10, 'name': 'tango10', 'status': 'locked', 'pistol': 'Off','codes': 0},
    {'id': 11, 'name': 'tango11', 'status': 'locked', 'pistol': 'Off','codes': 0},
    {'id': 12, 'name': 'tango12', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 13, 'name': 'tango13', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 14, 'name': 'raspibalizaproveedores', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 15, 'name': 'tango15', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 16, 'name': 'raspi16', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 17, 'name': 'raspi17', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 18, 'name': 'tango18', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 19, 'name': 'tango19', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 20, 'name': 'tango20', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 21, 'name': 'baliza-disca', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 22, 'name': 'vehiculos', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
]

# Device health tracking - stores health data from devices
device_health = {}  # device_name -> health_data with last_seen

# Pending commands queue - stores commands waiting for device pickup
pending_commands = {}  # device_name -> {'command': 'reboot', 'issued_at': ...}

# Timeout for considering a device offline (seconds)
DEVICE_TIMEOUT_SECONDS = 60

def is_device_online(device_name):
    """Check if device has reported health within timeout period"""
    health = device_health.get(device_name)
    if not health or 'last_seen' not in health:
        return False
    try:
        last_seen = datetime.fromisoformat(health['last_seen'])
        return (datetime.now() - last_seen).total_seconds() < DEVICE_TIMEOUT_SECONDS
    except:
        return False

# ============================================
# Authentication
# ============================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# C# API Helper Functions
def fetch_ticket(ticket_code):
    """GET /Ticket/Validate"""
    try:
        apikey = keys['key1']
        header = {
            'X-API-Key': f'{apikey}',
            'Content-Type': "application/json"
        }
        payload = {'code': ticket_code}
        print(payload)
        resp = requests.post(f"{CARNAVAL_API_URL}/Ticket/Validate",
                             params= payload,
                             headers= header,
                             timeout=API_TIMEOUT)
        data = resp.json()
        return data.get('result') if data.get('success') else None
    except:
        return None


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

# ============================================
# Login / Logout Routes
# ============================================

@app.route('/login', methods=['GET'])
def login_page():
    if session.get('user'):
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    try:
        resp = requests.post(
            f"{CARNAVAL_API_URL}/Auth",
            json={'username': username, 'password': password},
            timeout=API_TIMEOUT
        )
        data = resp.json()

        if resp.ok and data.get('success'):
            result = data['result']
            session['user'] = result['user']
            session['token'] = result['token']
            return redirect(url_for('home'))
        else:
            error = data.get('message', 'Invalid credentials')
            return render_template('login.html', error=error)
    except requests.exceptions.ConnectionError:
        return render_template('login.html', error='Cannot connect to API server')
    except Exception as e:
        return render_template('login.html', error='Login failed')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

# ============================================
# Protected Dashboard Routes
# ============================================

@app.route('/')
@login_required
def home():
    # Pass a variable to the HTML template
    return render_template('index.html', title='TURNSTILE MONITOR 2026', data=turnstiles)

@app.route('/fps')
@login_required
def fps():
    # Pass a variable to the HTML template
    return turnstiles

@app.route('/dashboard-data')
@login_required
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

    # Merge with local turnstile state and health info
    merged = []
    for ts in turnstiles:
        api_data = device_counts.get(ts['name'], {})
        # Try case-insensitive match for health data
        health = None
        online = False
        for device_name in device_health.keys():
            if device_name.lower() == ts['name'].lower():
                health = device_health[device_name]
                online = is_device_online(device_name)
                break
        if not health:
            health = {}
            online = False

        # Debug for Vehiculos
        if ts['name'] == 'Vehiculos':
            print(f"DEBUG Vehiculos: health={health}, online={online}")
            print(f"  Scanner data: {health.get('scanner', {})}")

        merged.append({
            'id': ts['id'],
            'name': ts['name'],
            'status': ts['status'],
            'pistol': ts['pistol'],
            'codes': api_data.get('peopleCount', 0),
            'gate': api_data.get('gateName', ''),
            'gateNickName': api_data.get('gateNickName', ''),
            'online': online,
            'health': {
                'scanner': health.get('scanner', {}).get('connected', False) if health else False,
                'scanner_disconnects': health.get('scanner', {}).get('disconnect_count', 0) if health else 0,
                'scanner_reconnects': health.get('scanner', {}).get('reconnect_count', 0) if health else 0,
                'display': health.get('display', {}).get('connected', False) if health else False,
                'network': health.get('network', {}).get('connected', False) if health else False,
                'cpu': health.get('system', {}).get('cpu_percent', 0) if health else 0,
                'memory': health.get('system', {}).get('memory_percent', 0) if health else 0,
                'temperature': health.get('system', {}).get('temperature') if health else None,
                'last_seen': health.get('last_seen') if health else None,
                'ip': health.get('ip') if health else None
            }
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

# ============================================
# Device API Routes (no login required)
# ============================================

@app.route('/api/hello', methods=['GET'])
def hello():
    name = request.args.get('name', default='World')
    ip = request.args.get('ip', default='localhost')
    print(f"hostname:{name} from IP:{ip}")
    print(ip)
    return jsonify({"message": f"Hello, {name} from IP:{ip}!"})

@app.route('/api/pistol', methods=['GET'])
def pistol():
    pistol_status = request.args.get('pistol', default='Off')
    ip = request.args.get('ip', default='localhost')
    device_name = request.args.get('device', default=None)

    # Support both old IP-based and new device name-based updates
    if device_name:
        # Find turnstile by device name (case-insensitive)
        for ts in turnstiles:
            if ts['name'].lower() == device_name.lower():
                ts['pistol'] = pistol_status
                print(f"Device:{device_name}, Pistol:{pistol_status}")
                return jsonify({"message": f"Pistol, {pistol_status} @ Device:{device_name}!"})
    else:
        # Legacy IP-based decoding
        decode_turnstile_pistol([ip, pistol_status])
        print(f"IP:{ip}, Pistol:{pistol_status}")
        return jsonify({"message": f"Pistol, {pistol_status} @ IP:{ip}!"})

    return jsonify({"error": "Device not found"}), 404

@app.route('/api/status', methods=['GET'])
def status():
    status_value = request.args.get('status', default='locked')
    ip = request.args.get('ip', default='localhost')
    device_name = request.args.get('device', default=None)

    # Support both old IP-based and new device name-based updates
    if device_name:
        # Find turnstile by device name (case-insensitive)
        for ts in turnstiles:
            if ts['name'].lower() == device_name.lower():
                ts['status'] = status_value
                print(f"Device:{device_name}, STATUS:{status_value}")
                return jsonify({"message": f"Status, {status_value} @ Device:{device_name}!"})
    else:
        # Legacy IP-based decoding
        decode_turnstile_status([ip, status_value])
        print(f"IP:{ip}, STATUS:{status_value}")
        return jsonify({"message": f"Status, {status_value} @ IP:{ip}!"})

    return jsonify({"error": "Device not found"}), 404

@app.route('/api/code', methods=['GET'])
def code():
    ip = request.args.get('ip', default='localhost')
    device_name = request.args.get('device', default=None)

    # Support both old IP-based and new device name-based updates
    if device_name:
        # Find turnstile by device name (case-insensitive)
        for ts in turnstiles:
            if ts['name'].lower() == device_name.lower():
                ts['codes'] += 1
                print(f"Device:{device_name}, New Code! Total:{ts['codes']}")
                return jsonify({"message": f"New Code @ Device:{device_name}!"})
    else:
        # Legacy IP-based decoding
        decode_turnstile_code([ip, 'code'])
        print(f"New Code @ IP:{ip}!")
        return jsonify({"message": f"New Code @ IP:{ip}!"})

    return jsonify({"error": "Device not found"}), 404

@app.route('/api/ticket', methods=['POST'])
def ticket():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    ticket_code = data.get('ticket')
    print(f"Validating ticket: {ticket_code}")

    if not ticket_code:
        return jsonify({'error': 'Ticket code required', 'status': 'error'}), 400

    result = fetch_ticket(ticket_code)
    print(f"Fetched ticket: {result}")

    if result:
        return jsonify({
            'status': 'success',
            'message': f'Ticket {ticket_code} found {result.get("m1", "")} - {result.get("m2", "")}',
            'deviceName': result.get('deviceName', 'Unknown'),
            'data': result
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Failed to validate ticket',
            'deviceName': 'System'
        })
# ============================================
# Ticket Event Notification Endpoint
# ============================================

@app.route('/api/ticket-event', methods=['POST'])
def ticket_event():
    """Receive ticket validation event from C# API and broadcast to clients"""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Broadcast to all connected Socket.IO clients
    socketio.emit('ticket_validated', {
        'code': data.get('code'),
        'device': data.get('device'),
        'deviceName': data.get('deviceName'),
        'gateName': data.get('gateName'),
        'status': data.get('status'),  # 'success', 'already_used', 'invalid', 'wrong_event'
        'message': data.get('message'),
        'timestamp': data.get('timestamp') or datetime.now().isoformat()
    })

    return jsonify({'success': True})

# ============================================
# Device Health Monitoring Endpoints
# ============================================

@app.route('/api/health', methods=['POST'])
def report_health():
    """Receive health report from device"""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    device_name = data.get('device')
    if not device_name:
        return jsonify({'error': 'Device name required'}), 400

    # Store health data with server-side timestamp
    device_health[device_name] = {
        **data,
        'last_seen': datetime.now().isoformat()
    }

    # Update turnstile status from health data (case-insensitive)
    scanner_connected = data.get('scanner', {}).get('connected', False)
    for ts in turnstiles:
        if ts['name'].lower() == device_name.lower():
            ts['online'] = True
            # Update pistol status based on scanner connection
            ts['pistol'] = 'On' if scanner_connected else 'Off'
            break

    print(f"Health report from {device_name}: CPU={data.get('system', {}).get('cpu_percent', 'N/A')}%, Scanner={scanner_connected}")
    return jsonify({'success': True})

@app.route('/api/health/<device_name>', methods=['GET'])
def get_health(device_name):
    """Get health data for a specific device"""
    health = device_health.get(device_name)
    if not health:
        return jsonify({'error': 'Device not found'}), 404
    return jsonify({
        **health,
        'online': is_device_online(device_name)
    })

@app.route('/api/health', methods=['GET'])
def get_all_health():
    """Get health data for all devices"""
    result = {}
    for name, health in device_health.items():
        result[name] = {
            **health,
            'online': is_device_online(name)
        }
    return jsonify(result)

# ============================================
# Remote Command Endpoints
# ============================================

@app.route('/api/commands/<device_name>', methods=['GET'])
def get_command(device_name):
    """Device polls for pending commands - returns and clears pending command"""
    cmd_data = pending_commands.pop(device_name, None)
    if cmd_data:
        print(f"Command '{cmd_data['command']}' picked up by {device_name}")
        return jsonify({'command': cmd_data['command']})
    return jsonify({'command': None})

@app.route('/api/commands/<device_name>', methods=['POST'])
def issue_command(device_name):
    """Admin issues a command to a device"""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    command = data.get('command')
    valid_commands = ['reboot', 'shutdown', 'restart_service', 'lcd_init']

    if command not in valid_commands:
        return jsonify({'error': f'Invalid command. Valid commands: {valid_commands}'}), 400

    # Check if device exists in our list
    device_exists = any(ts['name'] == device_name for ts in turnstiles)
    if not device_exists:
        return jsonify({'error': f'Unknown device: {device_name}'}), 404

    # Queue the command
    pending_commands[device_name] = {
        'command': command,
        'issued_at': datetime.now().isoformat()
    }

    print(f"Command '{command}' queued for {device_name}")
    return jsonify({
        'success': True,
        'message': f'{command} queued for {device_name}'
    })

@app.route('/api/commands', methods=['GET'])
def get_pending_commands():
    """Get all pending commands (admin view)"""
    return jsonify(pending_commands)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=False)
