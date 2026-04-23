document.addEventListener('DOMContentLoaded', function() {

    // delete account button (acceptation)
    const deleteAccountBtn = document.querySelector('span.delete-account-js');
    console.log(deleteAccountBtn);
    if (deleteAccountBtn) {
        deleteAccountBtn.style.cursor = 'pointer';
        deleteAccountBtn.style.transition = 'all 0.3s ease';

        deleteAccountBtn.addEventListener('click', function() {
            const form = this.closest('form');
        
            if (!this.classList.contains('confirm-state')) {
                this.dataset.originalText = this.innerText;
                this.innerText = "Na pewno? Kliknij ponownie";
                this.classList.replace('bg-warning', 'bg-danger');
                this.classList.remove('confirm-state', 'text-dark');
                this.classList.add('confirm-state');

                setTimeout(() => {
                    if (this.classList.contains('confirm-state')) {
                        this.innerText = this.dataset.originalText;
                        this.classList.replace('bg-danger', 'bg-warning');
                        this.classList.remove('confirm-state');
                    }
                }, 3000);

            } else {
                form.submit();
            }
        });
    }
    
    // change section buttons
    document.querySelectorAll(".switch-section-js").forEach(button => {
        button.addEventListener("click", function(e) {
            const sectionId = this.getAttribute('data-section');
            
            document.querySelectorAll('.content-section').forEach(section => section.style.display = 'none')

            const target = document.getElementById(sectionId);
            if (target) {
                target.style.display = 'block';
            }

            document.querySelectorAll('.switch-section-js').forEach(navBtn => {
                navBtn.classList.remove('active', 'btn-secondary');
                navBtn.classList.add('btn-outline-secondary');
            });

            this.classList.add('active', 'btn-secondary');
            this.classList.remove('btn-outline-secondary');
        });
    });

    function switchButtons(oldButton, newButton) {
        oldButton.classList.add("d-none");
        newButton.classList.remove("d-none");
    }

    // trigger edit profile
    document.querySelector(".edit-profile-data-js").addEventListener("click", function(e) {

        // hide edit button -> show accept button
        const newButton = document.querySelector(".confirm-profile-data-js");
        switchButtons(this, newButton)

        const fieldsData = {};
        
        // change fields to inputs
        document.querySelectorAll(".edit-field-js").forEach(field => {
            const fieldName = field.getAttribute('data-field');
            const valueSpan = field.querySelector(".field-value-js");

            const currentValue = valueSpan.innerText.trim();
            fieldsData[fieldName] = currentValue;

            valueSpan.innerHTML = `
                <input 
                    type="phone" 
                    placeholder="${currentValue}"
                >
            `;
        });

    });

    // accept new fields
    document.querySelector(".confirm-profile-data-js").addEventListener("click", function(e) {

        // hide correct button -> show edit button
        const newButton = document.querySelector(".edit-profile-data-js");
        switchButtons(this, newButton)
        
        // updatez
    });
}); 