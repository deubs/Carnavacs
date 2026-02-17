// Web Push subscription manager

(function() {
    var bellBtn = document.getElementById('notification-bell');
    if (!bellBtn) return;

    // Check browser support
    if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
        bellBtn.title = 'Push notifications not supported in this browser';
        bellBtn.disabled = true;
        return;
    }

    // Register service worker
    navigator.serviceWorker.register('/sw.js').then(function(reg) {
        reg.pushManager.getSubscription().then(function(sub) {
            if (sub) {
                bellBtn.classList.add('subscribed');
                bellBtn.title = 'Push notifications enabled (click to disable)';
            }
        });
    });

    bellBtn.addEventListener('click', function() {
        navigator.serviceWorker.ready.then(function(reg) {
            reg.pushManager.getSubscription().then(function(sub) {
                if (sub) {
                    sub.unsubscribe().then(function() {
                        fetch('/api/push/unsubscribe', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({endpoint: sub.endpoint})
                        });
                        bellBtn.classList.remove('subscribed');
                        bellBtn.title = 'Enable push notifications';
                    });
                } else {
                    subscribeToPush(reg);
                }
            });
        });
    });

    function subscribeToPush(reg) {
        Notification.requestPermission()
            .then(function(permission) {
                if (permission !== 'granted') {
                    alert('Notification permission denied');
                    return;
                }
                return fetch('/api/push/vapid-public-key');
            })
            .then(function(r) { if (r) return r.json(); })
            .then(function(data) {
                if (!data) return;
                if (!data.publicKey) {
                    alert('Push notifications not configured on the server');
                    return;
                }
                var key = urlBase64ToUint8Array(data.publicKey);
                return reg.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: key
                });
            })
            .then(function(sub) {
                if (!sub) return;
                return fetch('/api/push/subscribe', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(sub.toJSON())
                });
            })
            .then(function(resp) {
                if (resp && resp.ok) {
                    bellBtn.classList.add('subscribed');
                    bellBtn.title = 'Push notifications enabled (click to disable)';
                }
            })
            .catch(function(err) {
                console.error('Push subscription failed:', err);
            });
    }

    function urlBase64ToUint8Array(base64String) {
        var padding = '='.repeat((4 - base64String.length % 4) % 4);
        var base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
        var rawData = window.atob(base64);
        var outputArray = new Uint8Array(rawData.length);
        for (var i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }
})();
