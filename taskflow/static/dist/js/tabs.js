// tabs.js
document.addEventListener('DOMContentLoaded', () => {
    const tabButtons = document.querySelectorAll('[data-toggle="tab"]');
    tabButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();

            // Deactivate all tabs and hide all tab panes
            tabButtons.forEach(btn => {
                btn.classList.remove('bg-blue-500', 'text-white');
                btn.classList.add('text-blue-500', 'hover:bg-blue-500', 'hover:text-white');
                const targetId = btn.getAttribute('href').substring(1);
                document.getElementById(targetId).classList.add('hidden');
                document.getElementById(targetId).classList.remove('active');
            });

            // Activate clicked tab and show its pane
            button.classList.add('bg-blue-500', 'text-white');
            button.classList.remove('text-blue-500', 'hover:bg-blue-500', 'hover:text-white');
            const targetId = button.getAttribute('href').substring(1);
            document.getElementById(targetId).classList.remove('hidden');
            document.getElementById(targetId).classList.add('active');
        });
    });

    // Optionally, activate the first tab on page load if no active tab is set
    if (tabButtons.length > 0 && !document.querySelector('.tab-pane.active')) {
        tabButtons[0].click();
    }
});
