// card_widgets.js
document.addEventListener('DOMContentLoaded', () => {
    // Handle collapse functionality
    document.querySelectorAll('[data-card-widget="collapse"]').forEach(button => {
        button.addEventListener('click', () => {
            const card = button.closest('.shadow-lg.rounded-lg'); // Assuming the card has these classes
            if (card) {
                const cardBody = card.querySelector('.p-6'); // Assuming card body has 'p-6'
                if (cardBody) {
                    cardBody.classList.toggle('hidden');
                    button.querySelector('i').classList.toggle('fa-minus');
                    button.querySelector('i').classList.toggle('fa-plus');
                }
            }
        });
    });

    // Handle remove functionality
    document.querySelectorAll('[data-card-widget="remove"]').forEach(button => {
        button.addEventListener('click', () => {
            const card = button.closest('.shadow-lg.rounded-lg'); // Assuming the card has these classes
            if (card) {
                card.remove();
            }
        });
    });
});
