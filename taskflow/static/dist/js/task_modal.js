document.addEventListener('DOMContentLoaded', function () {
    const taskUpdateModal = document.getElementById('taskUpdateModal');
    const openModalButtons = document.querySelectorAll('.fa-pen');
    const closeModalButton = taskUpdateModal.querySelector('[data-dismiss="modal"]');

    if (taskUpdateModal && openModalButtons && closeModalButton) {
        openModalButtons.forEach(function (button) {
            button.addEventListener('click', function () {
                taskUpdateModal.classList.remove('hidden');
            });
        });

        closeModalButton.addEventListener('click', function () {
            taskUpdateModal.classList.add('hidden');
        });

        window.addEventListener('click', function (event) {
            if (event.target == taskUpdateModal) {
                taskUpdateModal.classList.add('hidden');
            }
        });
    }
});