document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.querySelector('aside');
    const sidebarToggleButton = document.querySelector('[data-widget="pushmenu"]');

    if (sidebar && sidebarToggleButton) {
        sidebarToggleButton.addEventListener('click', function () {
            sidebar.classList.toggle('w-64');
            sidebar.classList.toggle('w-0');
            sidebar.classList.toggle('hidden'); // Add hidden class for better hiding
        });
    }
});
