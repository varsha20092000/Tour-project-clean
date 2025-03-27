document.addEventListener('DOMContentLoaded', () => {
    const loveIcons = document.querySelectorAll('.love-icon');

    // Search Functionality
    document.getElementById('searchButton').addEventListener('click', function () {
        const input = document.getElementById('searchInput').value.toLowerCase();
        const cards = document.querySelectorAll('.card');
        let found = false;

        cards.forEach(card => {
            const destinationName = card.querySelector('h3').textContent.toLowerCase();
            const destinationId = card.getAttribute('data-id'); // Get data-id

            if (destinationName.includes(input) && destinationId) {
                console.log(`Navigating to: /destinations/${destinationId}`);
                window.location.href = `/destinations/${destinationId}`; // Redirect to details page
                found = true;
            } else if (!destinationId) {
                console.warn(`Card with name "${destinationName}" is missing data-id.`);
            }
        });

        if (!found) {
            alert('Destination not found!');
        }
    });

    // Add click event listeners to love icons
    loveIcons.forEach(icon => {
        icon.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent triggering any parent click events
            const heart = icon.querySelector('i');
            const isLiked = heart.classList.contains('fas');

            // Toggle the heart icon
            heart.classList.toggle('far', isLiked);
            heart.classList.toggle('fas', !isLiked);

            // Additional logic for "liked" destinations can be added here if needed
        });
    });
});

