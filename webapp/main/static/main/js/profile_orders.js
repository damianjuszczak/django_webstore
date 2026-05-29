document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll(".cancel-order-js").forEach(orderBtn => {
        orderBtn.addEventListener('click', async function(e) {
            e.preventDefault();
            const orderId = this.dataset.orderid;
            try {
                const response = await fetch(`/api/order/cancel/${orderId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();
                if (response.ok && data.status === 'success') {
                    showNotification('success', data.message);
                } else {
                    showNotification('error', data.message);
                }
            } catch (error) {
                showNotification('error', 'Błąd połączenia z serwerem.')
            }
        });
    });
    document.querySelectorAll(".renew-order-js").forEach(renewBtn => {
        renewBtn.addEventListener('click', async function(e) {
            e.preventDefault();
            const orderId = this.dataset.orderid;
            try {
                const response = await fetch(`/api/order/renew/${orderId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();
            if (response.ok && data.status === 'success') {
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                } else {
                    showNotification('success', data.message);
                }
            } else {
                showNotification('error', data.message);
            }
        } catch (error) {
            showNotification('error', 'Błąd połączenia z serwerem.');
        }
    });
});
});