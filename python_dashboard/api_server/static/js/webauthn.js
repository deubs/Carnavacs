/* WebAuthn / Passkey helpers */

function bufferToBase64url(buffer) {
    var bytes = new Uint8Array(buffer);
    var str = '';
    for (var i = 0; i < bytes.length; i++) str += String.fromCharCode(bytes[i]);
    return btoa(str).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function base64urlToBuffer(base64url) {
    var base64 = base64url.replace(/-/g, '+').replace(/_/g, '/');
    while (base64.length % 4) base64 += '=';
    var binary = atob(base64);
    var bytes = new Uint8Array(binary.length);
    for (var i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    return bytes.buffer;
}

function showWebauthnToast(message, level) {
    var container = document.getElementById('toast-container');
    if (!container) { alert(message); return; }
    var cls = level === 'success' ? 'toast-success' : level === 'warning' ? 'toast-warning' : 'toast-error';
    var icon = level === 'success' ? '&#10003;' : '&#9888;';
    var toast = document.createElement('div');
    toast.className = 'toast ' + cls;
    toast.innerHTML = '<span class="toast-icon">' + icon + '</span>' +
        '<div class="toast-content"><span class="toast-message">' + message + '</span></div>';
    container.appendChild(toast);
    setTimeout(function() {
        toast.classList.add('toast-fade-out');
        setTimeout(function() { toast.remove(); }, 300);
    }, 4000);
}

async function registerPasskey() {
    try {
        var optResp = await fetch('/webauthn/register/options', { method: 'POST' });
        if (!optResp.ok) throw new Error('Failed to get registration options');
        var options = await optResp.json();

        options.challenge = base64urlToBuffer(options.challenge);
        options.user.id = base64urlToBuffer(options.user.id);
        if (options.excludeCredentials) {
            options.excludeCredentials = options.excludeCredentials.map(function(c) {
                return { id: base64urlToBuffer(c.id), type: c.type };
            });
        }

        var credential = await navigator.credentials.create({ publicKey: options });

        var body = {
            id: bufferToBase64url(credential.rawId),
            rawId: bufferToBase64url(credential.rawId),
            type: credential.type,
            response: {
                attestationObject: bufferToBase64url(credential.response.attestationObject),
                clientDataJSON: bufferToBase64url(credential.response.clientDataJSON),
            },
        };

        var verResp = await fetch('/webauthn/register/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        var result = await verResp.json();

        if (result.success) {
            showWebauthnToast('Passkey registered', 'success');
        } else {
            showWebauthnToast(result.error || 'Registration failed', 'error');
        }
    } catch (e) {
        if (e.name !== 'NotAllowedError') {
            showWebauthnToast('Registration error: ' + e.message, 'error');
        }
    }
}

async function loginWithPasskey() {
    try {
        var optResp = await fetch('/webauthn/login/options', { method: 'POST' });
        if (!optResp.ok) throw new Error('Failed to get login options');
        var options = await optResp.json();

        options.challenge = base64urlToBuffer(options.challenge);
        if (options.allowCredentials) {
            options.allowCredentials = options.allowCredentials.map(function(c) {
                return { id: base64urlToBuffer(c.id), type: c.type };
            });
        }

        var assertion = await navigator.credentials.get({ publicKey: options });

        var body = {
            id: bufferToBase64url(assertion.rawId),
            rawId: bufferToBase64url(assertion.rawId),
            type: assertion.type,
            response: {
                authenticatorData: bufferToBase64url(assertion.response.authenticatorData),
                clientDataJSON: bufferToBase64url(assertion.response.clientDataJSON),
                signature: bufferToBase64url(assertion.response.signature),
                userHandle: assertion.response.userHandle
                    ? bufferToBase64url(assertion.response.userHandle)
                    : null,
            },
        };

        var verResp = await fetch('/webauthn/login/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        var result = await verResp.json();

        if (result.success) {
            window.location.href = result.redirect || '/';
        } else {
            showLoginError(result.error || 'Authentication failed');
        }
    } catch (e) {
        if (e.name !== 'NotAllowedError') {
            showLoginError('Passkey error: ' + e.message);
        }
    }
}

function showLoginError(message) {
    // On login page: show error in the login-error div
    var errDiv = document.querySelector('.login-error');
    if (!errDiv) {
        errDiv = document.createElement('div');
        errDiv.className = 'login-error';
        var card = document.querySelector('.login-card');
        var form = card && card.querySelector('form');
        if (form) card.insertBefore(errDiv, form);
        else return alert(message);
    }
    errDiv.textContent = message;
    errDiv.style.display = '';
}
