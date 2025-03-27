document.addEventListener("DOMContentLoaded", () => {
    // Carousel functionality
    let currentIndex = 0;
    const items = document.querySelectorAll('.carousel-item');
    const dots = document.querySelectorAll('.dot');
    const totalItems = items.length;

    function showSlide(index) {
        const inner = document.querySelector('.carousel-inner');
        if (inner) {
            inner.style.transform = `translateX(-${index * 100}%)`;
        }
        
        dots.forEach(dot => dot.classList.remove('active'));
        if (dots[index]) {
            dots[index].classList.add('active');
        }
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalItems;
        showSlide(currentIndex);
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        showSlide(currentIndex);
    }

    let slideInterval = null;
    if (totalItems > 0) {
        slideInterval = setInterval(nextSlide, 3000);
    }

    // Stop on hover - check if carousel exists
    const carousel = document.querySelector('.carousel');
    if (carousel) {
        carousel.addEventListener('mouseenter', () => {
            if (slideInterval !== null) {
                clearInterval(slideInterval);
            }
        });

        carousel.addEventListener('mouseleave', () => {
            slideInterval = setInterval(nextSlide, 3000);
        });
    }

    // Handle dots click
    if (dots.length) {
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                currentIndex = index;
                showSlide(currentIndex);
                if (slideInterval !== null) {
                    clearInterval(slideInterval);
                }
                slideInterval = setInterval(nextSlide, 3000);
            });
        });
    }

    // Heart icon functionality for packages.
    // This code stores package data in localStorage under "likedPackages"
    // so that the "Favorite Packages" page can display them.
    const heartIcons = document.querySelectorAll('.heart-icon');
    // Load existing liked packages from localStorage
    let likedPackages = {};
    const storedPackages = localStorage.getItem('likedPackages');
    if (storedPackages) {
        try {
            likedPackages = JSON.parse(storedPackages);
        } catch (error) {
            console.error('Error parsing likedPackages:', error);
        }
    }

    if (heartIcons.length) {
        heartIcons.forEach(icon => {
            // Retrieve the unique identifier from a data attribute (e.g., data-id)
            const uniqueId = icon.dataset.id;
            // On page load, if this package is liked, mark the icon as filled.
            if (uniqueId && likedPackages[uniqueId]) {
                icon.classList.add('filled');
            } else {
                icon.classList.remove('filled');
            }
            
            // Add click event to toggle the filled state and update localStorage.
            icon.addEventListener('click', function () {
                icon.classList.toggle('filled');  // Toggle 'filled' class on click
                
                // Get the parent card element containing the package details.
                const card = icon.closest('.card');
                if (!card) return;
                
                // Extract package details from the card.
                // Adjust these selectors as needed based on your actual markup.
                const packageNameElem = card.querySelector('h3');
                const packageName = packageNameElem ? packageNameElem.innerText.trim() : '';
                // Assuming description is inside .content h3 (if present)
                const packageDescElem = card.querySelector('.content h3');
                const packageDescription = packageDescElem ? packageDescElem.innerText.trim() : '';
                // Assuming price is in the first paragraph inside .content
                const packagePriceElem = card.querySelector('.content p');
                const packagePrice = packagePriceElem ? packagePriceElem.innerText.trim() : '';
                const packageImageElem = card.querySelector('img');
                const packageImage = packageImageElem ? packageImageElem.src : '';

                const pkg = {
                    id: uniqueId,
                    name: packageName,
                    description: packageDescription,
                    price: packagePrice,
                    image: packageImage
                };

                // Update likedPackages based on whether the icon is filled.
                if (icon.classList.contains('filled')) {
                    likedPackages[uniqueId] = pkg;
                } else {
                    delete likedPackages[uniqueId];
                }
                localStorage.setItem('likedPackages', JSON.stringify(likedPackages));
            });
        });
    }
});


