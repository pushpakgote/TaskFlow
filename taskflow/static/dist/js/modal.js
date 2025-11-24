// modal.js
document.addEventListener('DOMContentLoaded', () => {
    const modalButton = document.querySelector('[data-toggle="modal"]');
    const modal = document.getElementById('modal-default');
    const closeModalButton = modal.querySelector('[data-dismiss="modal"]');

    if (modalButton && modal && closeModalButton) {
        modalButton.addEventListener('click', () => {
            modal.classList.remove('hidden');
        });

        closeModalButton.addEventListener('click', () => {
            modal.classList.add('hidden');
        });

        // Close modal when clicking outside of it
        modal.addEventListener('click', (event) => {
            if (event.target === modal) {
                modal.classList.add('hidden');
            }
        });
    }
});
