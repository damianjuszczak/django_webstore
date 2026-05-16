document.addEventListener("DOMContentLoaded", function() {
    
    // login api
    const loginForm = document.querySelector("#login-form");
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => handleAuthSubmit(e, '/api/auth/login/'));
    }

    // register api
    const registerForm = document.querySelector('#register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => handleAuthSubmit(e, '/api/auth/register/'));
    }

    const logoutForms = document.querySelectorAll('.logout-form');
    logoutForms.forEach(form => {
        form.addEventListener("submit", async function(e) {
            e.preventDefault();

            try {
                const response = await fetch(this.action, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();
                if (data.status === 'success') {
                    window.location.href = data.redirect_url;
                }
            } catch(error) {
                showNotification('error', 'Coś poszło nie tak, spróbuje ponownie.')
            }
        });
    });

    async function handleAuthSubmit(e, url) {
        e.preventDefault();

        const form = e.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerText;

        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Czekaj...';

        try {
            const formData = new FormData(form)
            const response = await fetch(url, {
                method: "POST",
                body: formData,
                'X-Requested-With': 'XMLHttpRequest'
            })
            const data = await response.json();

            if (response.ok && data.status === 'success') {
                window.location.href = data.redirect_url;
            } else {
                showNotification('error', data.message);
                submitBtn.disabled = false;
                submitBtn.innerText = originalBtnText;
            }
        } catch (error) {
            submitBtn.disabled = false;
            submitBtn.innerText = originalBtnText;
        }
    }
});