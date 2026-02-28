"""JSON file-based WebAuthn credential storage."""

import json
import os
import fcntl

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'webauthn_credentials.json')


def _load():
    if not os.path.exists(CREDENTIALS_FILE):
        return {'credentials': []}
    with open(CREDENTIALS_FILE, 'r') as f:
        return json.load(f)


def _save(data):
    tmp = CREDENTIALS_FILE + '.tmp'
    with open(tmp, 'w') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        json.dump(data, f, indent=2)
        fcntl.flock(f, fcntl.LOCK_UN)
    os.replace(tmp, CREDENTIALS_FILE)


def save_credential(credential_id, public_key, sign_count, user_id, username, user_data):
    data = _load()
    data['credentials'].append({
        'credential_id': credential_id,
        'public_key': public_key,
        'sign_count': sign_count,
        'user_id': user_id,
        'username': username,
        'user_data': user_data,
    })
    _save(data)


def get_credentials_for_user(username):
    data = _load()
    return [c for c in data['credentials'] if c['username'] == username]


def get_credential_by_id(credential_id):
    data = _load()
    for c in data['credentials']:
        if c['credential_id'] == credential_id:
            return c
    return None


def get_all_credentials():
    return _load()['credentials']


def update_sign_count(credential_id, new_count):
    data = _load()
    for c in data['credentials']:
        if c['credential_id'] == credential_id:
            c['sign_count'] = new_count
            break
    _save(data)
