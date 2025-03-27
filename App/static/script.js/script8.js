document.addEventListener('DOMContentLoaded', () => {
    const loveIcons = document.querySelectorAll('.love-icon');

    // Load the liked destinations object from localStorage (or initialize it)
    let likedDestinations = {};
    const storedData = localStorage.getItem('likedDestinations');
    if (storedData) {
        try {
            likedDestinations = JSON.parse(storedData);
        } catch (error) {
            console.error('Error parsing likedDestinations:', error);
        }
    }

    // Update icons based on whether the destination is liked
    loveIcons.forEach(icon => {
        const heart = icon.querySelector('i');
        const destKey = icon.dataset.name; // ideally use a unique id or slug

        if (likedDestinations[destKey]) {
            heart.classList.remove('far');
            heart.classList.add('fas');
        } else {
            heart.classList.remove('fas');
            heart.classList.add('far');
        }

        icon.addEventListener('click', (event) => {
            event.stopPropagation();

            const heart = icon.querySelector('i');
            const destKey = icon.dataset.name;
            // Create a destination object using the dataset values
            const destinationData = {
                name: icon.dataset.name,
                description: icon.dataset.description,
                location: icon.dataset.location,
                image: icon.dataset.image
            };

            // Toggle the liked state in our collection
            if (likedDestinations[destKey]) {
                // Remove destination from likedDestinations
                delete likedDestinations[destKey];
                heart.classList.remove('fas');
                heart.classList.add('far');
            } else {
                // Add destination to likedDestinations
                likedDestinations[destKey] = destinationData;
                heart.classList.remove('far');
                heart.classList.add('fas');
            }

            // Save the updated likedDestinations collection back to localStorage
            localStorage.setItem('likedDestinations', JSON.stringify(likedDestinations));
        });
    });
});
