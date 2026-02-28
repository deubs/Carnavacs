// Service Worker for Web Push notifications

self.addEventListener('push', function(event) {
    var data = {title: 'Dashboard Alert', body: '', level: 'info'};
    if (event.data) {
        try { data = event.data.json(); } catch (e) { data.body = event.data.text(); }
    }

    var icon = data.level === 'critical' ? '/static/img/alert-red.png' :
               data.level === 'warning' ? '/static/img/alert-orange.png' :
               '/static/img/alert-green.png';

    event.waitUntil(
        self.registration.showNotification(data.title, {
            body: data.body,
            icon: icon,
            badge: icon,
            tag: data.level,
            renotify: true,
        })
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(
        clients.matchAll({type: 'window', includeUncontrolled: true}).then(function(clientList) {
            for (var i = 0; i < clientList.length; i++) {
                if (clientList[i].url.indexOf('/') !== -1 && 'focus' in clientList[i]) {
                    return clientList[i].focus();
                }
            }
            return clients.openWindow('/');
        })
    );
});
