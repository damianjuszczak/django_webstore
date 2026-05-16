document.addEventListener('DOMContentLoaded', function() {
    function switchButtons(buttonToHide, buttonToShow) {
        if (buttonToHide && buttonToShow) {
            buttonToHide.classList.add('d-none');
            buttonToShow.classList.remove('d-none');
        }
    }
    function hideBadges(forceHide) {
        const badges = document.querySelectorAll(".badge-visibility-js");
        badges.forEach(badge => {
            if (forceHide) {
                badge.classList.add('d-none');
            } else {
                badge.classList.remove('d-none');
            }
        });
    }

    const deleteAccountBtn = document.querySelector('span#delete-account-js');

    if (deleteAccountBtn) {
        deleteAccountBtn.style.cursor = 'pointer';
        deleteAccountBtn.style.transition = 'all 0.3s ease';

        deleteAccountBtn.addEventListener('click', async function() {
            const form = this.closest('form');

            if (!this.classList.contains('confirm-state')) {
                this.dataset.originalText = this.innerText;
                this.innerText = "Na pewno? Kliknij ponownie";

                this.classList.replace('bg-warning', 'bg-danger');
                this.classList.remove('text-dark');
                this.classList.add('confirm-state');

                setTimeout(() => {
                    if (this.classList.contains('confirm-state')) {
                        this.innerText = this.dataset.originalText;

                        this.classList.replace('bg-danger', 'bg-warning');
                        this.classList.remove('confirm-state');
                    }
                }, 3000);

            } else {
                try {
                    const response = await fetch(form.action, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });

                    if (response.redirected) {
                        window.location.href = response.url;
                    }

                } catch (error) {
                    console.error("Błąd sieci:", error);
                }
            }
        });
    }

    const editButton = document.querySelector(".edit-profile-data-js");
    const confirmButton = document.querySelector(".confirm-profile-data-js");
    const dataLoadingSpinner = document.querySelector(".data-lodaing-spinner-js");

    if (editButton && confirmButton) {
        editButton.addEventListener("click", function() {
            switchButtons(this, confirmButton);
            hideBadges(true);

            document.querySelectorAll(".edit-field-js").forEach(field => {
                const valueSpan = field.querySelector(".field-value-js");

                if (!valueSpan) return;
                valueSpan.dataset.oldvalue = field.dataset.field;
                valueSpan.innerHTML = `
                    <input 
                        type="${field.dataset.field}"
                        name="${field.dataset.inputname}"
                        class="form-control"
                        value="${field.dataset.oldvalue}"
                        placeholder="${field.dataset.oldvalue}"
                    >
                `;
            });
        });

        confirmButton.addEventListener("click", async function() {
            const formData = new FormData();
            const fieldsToUpdate = {};
            document.querySelectorAll(".edit-field-js").forEach(field => {
                const valueSpan = field.querySelector(".field-value-js");
                if (!valueSpan) return;

                const input = valueSpan.querySelector("input");
                if (input) {
                    const newValue = input.value.trim();
                    const oldValue = valueSpan.dataset.oldValue;
                    const finalValue = newValue !== "" ? newValue : (oldValue || "");

                    const fieldName = input.getAttribute("name");
                    console.log(fieldName, finalValue)
                    if (fieldName) {
                        formData.append(fieldName, finalValue);
                    }

                    valueSpan.innerText = finalValue;
                    const nearestBadge = field.querySelector(".badge-visibility-js");
                    if (nearestBadge) {
                        finalValue !== "" ? nearestBadge.classList.add("d-none") : nearestBadge.classList.remove("d-none");
                    }
                    delete valueSpan.dataset.oldValue;
                }
            });
            
            switchButtons(this, dataLoadingSpinner);
            try {
                const response = await fetch("/api/profile/profile-change-info/", {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    }
                });

                const data = await response.json();
                if (response.ok && data.status === 'success') {
                    showNotification('success', data.message);
                } else {
                    window.location.href = data.redirect_url;
                }
            } catch (error) {
                showNotification('error', 'Błąd połączenia z serwerem.')
            }
            switchButtons(dataLoadingSpinner, editButton);
        });
    }
});