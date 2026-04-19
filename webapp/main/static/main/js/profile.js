document.addEventListener('DOMContentLoaded', function() {
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

    const warnings = document.querySelectorAll('.expandable-warning');
    warnings.forEach(warning => {
        warning.addEventListener('click', function() {
            this.classList.toggle('expanded');
            if (this.classList.contains('expanded')) {
                setTimeout(() => {
                    this.classList.remove('expanded');
                }, 3000);
            }
        });
    });
    
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

});