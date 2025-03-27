document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll(".carousel-image");
    const dots = document.querySelectorAll(".dot");
    const prevButton = document.querySelector(".prev");
    const nextButton = document.querySelector(".next");

    let currentIndex = 0;
    let autoSlideInterval;

    // Function to update the carousel display
    function updateCarousel() {
        images.forEach((img, index) => {
            img.style.display = index === currentIndex ? "block" : "none";
        });

        dots.forEach((dot, index) => {
            dot.classList.toggle("active", index === currentIndex);
        });
    }

    // Function to go to the next image
    function nextImage() {
        currentIndex = (currentIndex + 1) % images.length;
        updateCarousel();
    }

    // Event listeners for buttons
    prevButton.addEventListener("click", () => {
        clearInterval(autoSlideInterval); // Pause auto-slide when manually navigating
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        updateCarousel();
        startAutoSlide(); // Restart auto-slide
    });

    nextButton.addEventListener("click", () => {
        clearInterval(autoSlideInterval); // Pause auto-slide when manually navigating
        nextImage();
        startAutoSlide(); // Restart auto-slide
    });

    // Event listeners for dots
    dots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
            clearInterval(autoSlideInterval); // Pause auto-slide when manually navigating
            currentIndex = index;
            updateCarousel();
            startAutoSlide(); // Restart auto-slide
        });
    });

    // Function to start auto-sliding
    function startAutoSlide() {
        autoSlideInterval = setInterval(nextImage, 3000); // Change image every 3 seconds
    }

    // Initialize the carousel and start auto-slide
    updateCarousel();
    startAutoSlide();
});
