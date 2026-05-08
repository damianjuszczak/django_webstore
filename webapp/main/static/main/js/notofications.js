document.addEventListener('DOMContentLoaded', function() {
    const notifications = document.querySelectorAll('.notification-item');

    notifications.forEach(notification => {
        const removeNotification = () => {
            notification.style.opacity = '0';
            notification.style.transition = 'opacity 0.5s ease';
            setTimeout(() => notification.remove(), 500);
        };

        const autoHideTimeout = setTimeout(removeNotification, 1750);
    });
});