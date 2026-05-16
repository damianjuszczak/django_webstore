let notificationTimer = null;

function showNotification(tag, message) {
    const container = document.querySelector(".notifications-container");
    if (!container) return;

    let notification = container.querySelector(".notification-item");
    
    if (!notification) {
        notification = document.createElement("div");
        notification.className = "notification-item";
        container.appendChild(notification);
    }

    if (notificationTimer) {
        clearTimeout(notificationTimer);
    }

    notification.style.transition = 'none';
    notification.className = "notification-item";
    notification.classList.add(`notification-${tag}`);
    notification.textContent = message;
    
    void notification.offsetWidth; 
    
    notification.style.transition = 'opacity 0.5s ease';
    notification.style.opacity = '1';

    const removeNotification = () => {
        notification.style.opacity = '0';

        notificationTimer = setTimeout(() => {
            notification.textContent = "";
            notification.className = "notification-item";
        }, 500);
    };

    notificationTimer = setTimeout(removeNotification, 3000);
}

document.addEventListener('DOMContentLoaded', function() {
    const notifications = document.querySelectorAll('.notification-item');
    
    notifications.forEach(notification => {
        if (notification.textContent.trim() !== "") {
            notification.style.opacity = '1';
            
            setTimeout(() => {
                notification.style.transition = 'opacity 0.5s ease';
                notification.style.opacity = '0';
                
                setTimeout(() => {
                    notification.textContent = "";
                    notification.className = "notification-item";
                }, 500);
            }, 3000);
        }
    });
});