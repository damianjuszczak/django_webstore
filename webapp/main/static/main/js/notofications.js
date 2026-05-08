function setupNotifications(container) {
    const notifications = container.querySelectorAll('.notification-item');

    notifications.forEach(notification => {
        const removeNotification = () => {
            notification.style.opacity = '0';
            notification.style.transition = 'opacity 0.5s ease';
            setTimeout(() => notification.remove(), 500);
        };

        const autoHideTimeout = setTimeout(removeNotification, 1750);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    setupNotifications(document);
});

document.body.addEventListener('htmx:afterSwap', function(event) {
    setupNotifications(event.detail.target);
});