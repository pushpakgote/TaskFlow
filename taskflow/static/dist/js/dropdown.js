document.addEventListener('DOMContentLoaded', function () {
    const userMenuButton = document.getElementById('user-menu-button');
    const userMenu = userMenuButton ? userMenuButton.closest('.relative').querySelector('[role="menu"]') : null;

    const notificationsMenuButton = document.getElementById('notifications-menu-button');
    const notificationsMenu = notificationsMenuButton ? notificationsMenuButton.closest('.relative').querySelector('[role="menu"]') : null;

    function toggleDropdown(menu) {
        if (menu) {
            menu.classList.toggle('hidden');
        }
    }

    if (userMenuButton) {
        userMenuButton.addEventListener('click', function (event) {
            event.stopPropagation();
            toggleDropdown(userMenu);
            if (notificationsMenu && !notificationsMenu.classList.contains('hidden')) {
                toggleDropdown(notificationsMenu);
            }
        });
    }

    if (notificationsMenuButton) {
        notificationsMenuButton.addEventListener('click', function (event) {
            event.stopPropagation();
            toggleDropdown(notificationsMenu);
            if (userMenu && !userMenu.classList.contains('hidden')) {
                toggleDropdown(userMenu);
            }
        });
    }

    document.addEventListener('click', function (event) {
        if (userMenu && !userMenu.classList.contains('hidden') && !userMenu.contains(event.target) && !userMenuButton.contains(event.target)) {
            toggleDropdown(userMenu);
        }
        if (notificationsMenu && !notificationsMenu.classList.contains('hidden') && !notificationsMenu.contains(event.target) && !notificationsMenuButton.contains(event.target)) {
            toggleDropdown(notificationsMenu);
        }
    });
});