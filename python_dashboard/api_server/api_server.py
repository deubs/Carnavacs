from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room
from functools import wraps
from dotenv import load_dotenv
import requests
import json
import os
from datetime import datetime
import threading
import time
import psutil
import websocket as ws_client
# import cli_api_status

from notifications import NotificationDispatcher
from notifications.channels.telegram import TelegramChannel
from notifications.channels.slack import SlackChannel
from notifications.channels.webpush import WebPushChannel

load_dotenv()

# ============================================
# External Notification Channels
# ============================================

_channels = []

_tg_token = os.environ.get('TELEGRAM_BOT_TOKEN')
_tg_chat = os.environ.get('TELEGRAM_CHAT_ID')
if _tg_token and _tg_chat:
    _channels.append(TelegramChannel(_tg_token, _tg_chat))

_slack_url = os.environ.get('SLACK_WEBHOOK_URL')
if _slack_url:
    _channels.append(SlackChannel(_slack_url))

_vapid_private = os.environ.get('VAPID_PRIVATE_KEY')
_vapid_public = os.environ.get('VAPID_PUBLIC_KEY', '')
_vapid_mailto = os.environ.get('VAPID_MAILTO', 'mailto:admin@example.com')
webpush_channel = None
if _vapid_private:
    webpush_channel = WebPushChannel(_vapid_private, {'sub': _vapid_mailto})
    _channels.append(webpush_channel)

notify_dispatcher = NotificationDispatcher(_channels)

keys = {'key1': 'ed5976ff-2a98-470a-b90e-bf945d25c5c9',
'key2': '840c53ea-0467-4b52-b083-2de869d939a8',
'key3': '2329db1e-95e8-4265-986e-d02114dbf5dc'}

CARNAVAL_API_URL = os.environ.get('CARNAVAL_API_URL', 'http://192.168.40.101')
API_TIMEOUT = 5
APP_START_TIME = datetime.now()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'your_secret_key')
socketio = SocketIO(app)

turnstiles = [
    {'id': 1, 'name': 'tango01', 'ip': '192.168.40.201', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 2, 'name': 'tango02', 'ip': '192.168.40.202', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 3, 'name': 'tango03', 'ip': '192.168.40.203', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 4, 'name': 'tango04', 'ip': '192.168.40.204', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 5, 'name': 'tango05', 'ip': '192.168.40.205', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 6, 'name': 'tango06', 'ip': '192.168.40.206', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 7, 'name': 'tango07', 'ip': '192.168.40.207', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 8, 'name': 'tango08', 'ip': '192.168.40.208', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 9, 'name': 'tango09', 'ip': '192.168.40.209', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 10, 'name': 'tango10', 'ip': '192.168.40.210', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 11, 'name': 'tango11', 'ip': '192.168.40.211', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 12, 'name': 'tango12', 'ip': '192.168.40.212', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 13, 'name': 'tango13', 'ip': '192.168.40.213', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 14, 'name': 'raspibalizaproveedores', 'ip': '192.168.40.214', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 15, 'name': 'tango15', 'ip': '192.168.40.215', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 16, 'name': 'raspi16', 'ip': '192.168.40.216', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 17, 'name': 'raspi17', 'ip': '192.168.40.217', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 18, 'name': 'tango18', 'ip': '192.168.40.218', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 19, 'name': 'tango19', 'ip': '192.168.40.219', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 20, 'name': 'tango20', 'ip': '192.168.40.220', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 21, 'name': 'vehiculos', 'ip': '192.168.40.221', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
    {'id': 22, 'name': 'baliza-disca', 'ip': '192.168.40.222', 'status': 'locked', 'pistol': 'Off', 'codes': 0},
]

# Device health tracking - stores health data from devices
device_health = {}  # device_name -> health_data with last_seen

# Pending commands queue - stores commands waiting for device pickup (HTTP fallback)
pending_commands = {}  # device_name -> {'command': 'reboot', 'issued_at': ...}

# Socket.IO device connection tracking
connected_devices = {}  # device_name -> {'sid': sid, 'connected_at': iso_timestamp, 'ip': ip}

# Timeout for considering a device offline (seconds) - used as HTTP fallback
DEVICE_TIMEOUT_SECONDS = 15

def is_device_online(device_name):
    """Check if device is connected via Socket.IO or has recent HTTP health"""
    # Primary: check Socket.IO connection
    if device_name in connected_devices:
        return True
    # Fallback: check HTTP health timeout (for devices not yet migrated)
    health = device_health.get(device_name)
    if not health or 'last_seen' not in health:
        return False
    try:
        last_seen = datetime.fromisoformat(health['last_seen'])
        return (datetime.now() - last_seen).total_seconds() < DEVICE_TIMEOUT_SECONDS
    except:
        return False

# ============================================
# Infrastructure Server Health Monitoring
# ============================================

INFRASTRUCTURE_SERVERS = [
    {'name': 'Server1', 'ip': '192.168.40.100', 'url': 'http://192.168.40.100/api/health'},
    {'name': 'Server2', 'ip': '192.168.40.101', 'url': 'http://192.168.40.101/api/health'},
    {'name': 'linjack',  'ip': '192.168.40.244', 'url': 'http://192.168.40.244/health'},
    {'name': 'qbox1',   'ip': '192.168.40.102', 'url': 'http://192.168.40.102:8080/'},
    {'name': 'qbox2',   'ip': '192.168.40.103', 'url': 'http://192.168.40.103:8080/'},
]

server_health = {}
SERVER_CHECK_INTERVAL = 20
SERVER_CHECK_TIMEOUT = 4

def check_server_health(server):
    try:
        start = time.time()
        r = requests.get(server['url'], timeout=SERVER_CHECK_TIMEOUT)
        elapsed = int((time.time() - start) * 1000)
        metrics = {}
        try:
            data = r.json()
            sys_info = data.get('system') or data.get('result', {}).get('system')
            if sys_info:
                metrics = {
                    'cpuPercent': sys_info.get('cpuPercent', 0),
                    'memoryPercent': sys_info.get('memoryPercent', 0),
                    'diskPercent': sys_info.get('diskPercent', 0),
                }
        except Exception:
            pass
        return {
            'name': server['name'],
            'ip': server['ip'],
            'online': True,
            'status_code': r.status_code,
            'response_time_ms': elapsed,
            'last_checked': datetime.now().isoformat(),
            'metrics': metrics,
        }
    except Exception:
        return {
            'name': server['name'],
            'ip': server['ip'],
            'online': False,
            'status_code': 0,
            'response_time_ms': 0,
            'last_checked': datetime.now().isoformat(),
            'metrics': {},
        }

def server_health_monitor():
    while True:
        for server in INFRASTRUCTURE_SERVERS:
            result = check_server_health(server)
            prev = server_health.get(server['name'])
            if prev is not None:
                if prev['online'] and not result['online']:
                    notify_dispatcher.queue_event('server_offline', server['name'])
                elif not prev['online'] and result['online']:
                    notify_dispatcher.queue_event('server_online', server['name'])
            server_health[server['name']] = result
        time.sleep(SERVER_CHECK_INTERVAL)

threading.Thread(target=server_health_monitor, daemon=True).start()

# ============================================
# Quentro Box Socket.IO Client
# ============================================

QUENTRO_BOX_URL = os.environ.get('QUENTRO_BOX_URL', 'http://192.168.40.102:8080')

quentro_stats = {}  # {issued, used, void, enabled, reissued, newcode, all, ...}

def get_quentro_show_id():
    """Fetch the current event's quentroEventId from the C# API"""
    try:
        resp = requests.get(f"{CARNAVAL_API_URL}/Events/Current", timeout=API_TIMEOUT)
        data = resp.json()
        if data.get('success') and data.get('result'):
            show_id = data['result'].get('quentroEventId')
            if show_id:
                return str(show_id)
    except Exception as e:
        print(f"Failed to fetch quentroEventId: {e}")
    return None

def quentro_connection():
    """Connect to Quentro Box via raw WebSocket (Socket.IO v2 / Engine.IO v3 protocol).
    python-socketio v5 is incompatible with Socket.IO v2 servers, so we use websocket-client directly."""
    while True:
        show_id = get_quentro_show_id()
        if not show_id:
            print("Quentro: no quentroEventId found, retrying in 30s...")
            time.sleep(30)
            continue

        event_name = f'show-update-{show_id}'
        ws_url = QUENTRO_BOX_URL.replace('http://', 'ws://').replace('https://', 'wss://')
        ws_url += '/socket.io/?EIO=3&transport=websocket'

        print(f"Quentro: connecting to {QUENTRO_BOX_URL} for showId={show_id}")

        def on_message(ws, message):
            if message.startswith('0'):
                # Engine.IO open packet - send Socket.IO connect to namespace /
                ws.send('40')
            elif message == '40':
                # Socket.IO connected - send update-request event
                req = json.dumps({"showId": show_id})
                ws.send(f'42["update-request",{req}]')
                print(f"Quentro: connected, listening for {event_name}")
            elif message == '2':
                # Engine.IO ping - respond with pong
                ws.send('3')
            elif message.startswith('42'):
                try:
                    payload = json.loads(message[2:])
                    if len(payload) >= 2 and payload[0] == event_name:
                        quentro_stats.update(payload[1])
                except Exception:
                    pass

        def on_error(ws, error):
            print(f"Quentro: websocket error: {error}")

        def on_close(ws, *args):
            print("Quentro: disconnected")

        try:
            ws = ws_client.WebSocketApp(
                ws_url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.run_forever(ping_interval=0)  # Socket.IO v2 handles its own ping/pong
        except Exception as e:
            print(f"Quentro: connection failed: {e}")
        time.sleep(10)

threading.Thread(target=quentro_connection, daemon=True, name="QuentroBox").start()

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
    """GET /Ticket/Verify"""
    try:
        apikey = keys['key1']
        header = {
            'X-API-Key': f'{apikey}',
            'Content-Type': "application/json"
        }
        payload = {'code': ticket_code}
        print(payload)
        resp = requests.post(f"{CARNAVAL_API_URL}/Ticket/Verify",
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
# Server Health Endpoint (no login required)
# ============================================

@app.route('/health')
def health():
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    api_ok = False
    try:
        r = requests.get(f"{CARNAVAL_API_URL}/api/health", timeout=3)
        api_ok = r.status_code == 200
    except Exception:
        pass

    return jsonify({
        'status': 'healthy' if api_ok else 'degraded',
        'uptimeSeconds': int((datetime.now() - APP_START_TIME).total_seconds()),
        'timestamp': datetime.now().isoformat(),
        'system': {
            'cpuPercent': cpu,
            'memoryPercent': mem.percent,
            'memoryUsedMb': mem.used // (1024 * 1024),
            'memoryTotalMb': mem.total // (1024 * 1024),
            'diskPercent': disk.percent,
            'diskFreeMb': disk.free // (1024 * 1024),
        },
        'dependencies': {
            'carnavalApi': api_ok
        }
    })

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

    # Build device-to-peopleCount map from stats, keyed by IP (NroSerie)
    device_counts = {}
    if stats and stats.get('gates'):
        for gate in stats['gates']:
            for device in gate.get('accessDevices', []):
                device_counts[device['deviceName']] = {
                    'peopleCount': device['peopleCount'],
                    'gateName': gate['gateName'],
                    'gateNickName': device.get('gateNickName', ''),
                    'friendlyName': device.get('friendlyName')
                }

    # Merge with local turnstile state and health info
    merged = []
    for ts in turnstiles:
        # Match by IP (deviceName = NroSerie from DB)
        api_data = device_counts.get(ts['ip'], {})
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
            'friendlyName': api_data.get('friendlyName') or ts['name'],
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
            'remainingTickets': stats.get('remainingTickets', 0) if stats else 0,
            'quentroUsed': stats.get('quentroUsed', 0) if stats else 0,
            'collaboratorUsed': stats.get('collaboratorUsed', 0) if stats else 0,
            'collaboratorRemaining': stats.get('collaboratorRemaining', 0) if stats else 0,
        },
        'quentro': {
            'issued': quentro_stats.get('issued', 0),
            'used': quentro_stats.get('used', 0),
            'void': quentro_stats.get('void', 0),
            'all': quentro_stats.get('all', 0),
            'connected': bool(quentro_stats),
        },
        'turnstiles': merged,
        'servers': list(server_health.values()),
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
        ticket_status = result.get('ticketStatus', {})
        status_name = ticket_status.get('name', '')
        is_valid = result.get('isValid', False)

        return jsonify({
            'status': 'success' if is_valid else status_name.lower(),
            'message': f'{result.get("m1", "")} - {result.get("m2", "")}',
            'deviceName': result.get('gate', 'Unknown'),
            'usedDate': result.get('usedDate'),
            'gate': result.get('gate'),
            'ticketStatus': status_name,
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

    # Try Socket.IO push first, fall back to HTTP polling queue
    dev = connected_devices.get(device_name)
    if dev:
        socketio.emit('command', {'command': command},
                      namespace='/devices', to=device_name)
        print(f"Command '{command}' pushed to {device_name} via Socket.IO")
        return jsonify({
            'success': True,
            'message': f'{command} sent to {device_name}',
            'delivered': True
        })
    else:
        # Fallback: queue command for HTTP polling pickup
        pending_commands[device_name] = {
            'command': command,
            'issued_at': datetime.now().isoformat()
        }
        print(f"Command '{command}' queued for {device_name} (HTTP fallback)")
        return jsonify({
            'success': True,
            'message': f'{command} queued for {device_name}',
            'delivered': False
        })

@app.route('/api/commands', methods=['GET'])
def get_pending_commands():
    """Get all pending commands (admin view)"""
    return jsonify(pending_commands)

# ============================================
# Web Push Subscription Endpoints
# ============================================

@app.route('/api/push/vapid-public-key', methods=['GET'])
def push_vapid_key():
    """Return VAPID public key for client-side push subscription"""
    return jsonify({'publicKey': _vapid_public})

@app.route('/api/push/subscribe', methods=['POST'])
@login_required
def push_subscribe():
    """Store a push subscription"""
    if not webpush_channel:
        return jsonify({'error': 'Web Push not configured'}), 501
    sub = request.json
    if not sub or not sub.get('endpoint'):
        return jsonify({'error': 'Invalid subscription'}), 400
    webpush_channel.add_subscription(sub)
    return jsonify({'success': True})

@app.route('/api/push/unsubscribe', methods=['POST'])
@login_required
def push_unsubscribe():
    """Remove a push subscription"""
    if not webpush_channel:
        return jsonify({'error': 'Web Push not configured'}), 501
    data = request.json
    endpoint = data.get('endpoint') if data else None
    if not endpoint:
        return jsonify({'error': 'Endpoint required'}), 400
    webpush_channel.remove_subscription(endpoint)
    return jsonify({'success': True})

# ============================================
# Socket.IO Device Namespace (/devices)
# ============================================

@socketio.on('connect', namespace='/devices')
def device_connected():
    """Device connected - wait for register event with device name"""
    print(f"Device socket connected: {request.sid}")

@socketio.on('register', namespace='/devices')
def device_register(data):
    """Device registers itself after connecting"""
    device_name = data.get('device')
    ip = data.get('ip', 'unknown')
    if not device_name:
        return

    connected_devices[device_name] = {
        'sid': request.sid,
        'connected_at': datetime.now().isoformat(),
        'ip': ip
    }
    join_room(device_name, namespace='/devices')

    # Update turnstile online status
    for ts in turnstiles:
        if ts['name'].lower() == device_name.lower():
            ts['online'] = True
            break

    print(f"Device registered: {device_name} (sid={request.sid}, ip={ip})")
    # Notify browser clients
    socketio.emit('device_online', {'device': device_name, 'ip': ip})
    notify_dispatcher.queue_event('device_online', device_name)

@socketio.on('disconnect', namespace='/devices')
def device_disconnected():
    """Device disconnected - find by sid and mark offline"""
    sid = request.sid
    device_name = None
    for name, info in list(connected_devices.items()):
        if info['sid'] == sid:
            device_name = name
            del connected_devices[name]
            break

    if device_name:
        print(f"Device disconnected: {device_name}")
        # Notify browser clients
        socketio.emit('device_offline', {'device': device_name})
        notify_dispatcher.queue_event('device_offline', device_name)

@socketio.on('health', namespace='/devices')
def device_health_event(data):
    """Receive health report via Socket.IO (same logic as POST /api/health)"""
    device_name = data.get('device')
    if not device_name:
        return

    # Compare scanner state before overwriting
    prev = device_health.get(device_name)
    prev_scanner = prev.get('scanner', {}).get('connected', False) if prev else None
    new_scanner = data.get('scanner', {}).get('connected', False)

    if prev_scanner is not None and prev_scanner != new_scanner:
        if not new_scanner:
            notify_dispatcher.queue_event('scanner_disconnected', device_name)
        else:
            notify_dispatcher.queue_event('scanner_reconnected', device_name)

    # Store health data with server-side timestamp
    device_health[device_name] = {
        **data,
        'last_seen': datetime.now().isoformat()
    }

    # Update turnstile status from health data
    scanner_connected = new_scanner
    for ts in turnstiles:
        if ts['name'].lower() == device_name.lower():
            ts['online'] = True
            ts['pistol'] = 'On' if scanner_connected else 'Off'
            break

@socketio.on('status_change', namespace='/devices')
def device_status_change(data):
    """Device reports status change (locked/unlocked)"""
    device_name = data.get('device')
    status_value = data.get('status', 'locked')
    if not device_name:
        return

    for ts in turnstiles:
        if ts['name'].lower() == device_name.lower():
            ts['status'] = status_value
            break

    print(f"Device:{device_name}, STATUS:{status_value} (via Socket.IO)")
    # Notify browser clients for toast
    socketio.emit('turnstile_status', {'device': device_name, 'status': status_value})

@socketio.on('pistol_change', namespace='/devices')
def device_pistol_change(data):
    """Device reports pistol (scanner) change"""
    device_name = data.get('device')
    pistol_value = data.get('pistol', 'Off')
    if not device_name:
        return

    for ts in turnstiles:
        if ts['name'].lower() == device_name.lower():
            ts['pistol'] = pistol_value
            break

    print(f"Device:{device_name}, Pistol:{pistol_value} (via Socket.IO)")

@socketio.on('code_scanned', namespace='/devices')
def device_code_scanned(data):
    """Device reports a code was scanned"""
    device_name = data.get('device')
    if not device_name:
        return

    for ts in turnstiles:
        if ts['name'].lower() == device_name.lower():
            ts['codes'] += 1
            break

    print(f"Device:{device_name}, New Code (via Socket.IO)")

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=False)
