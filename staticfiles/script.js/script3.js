let currentSlideIndex = 0;
const slides = document.querySelectorAll('.carousel-slide');
const dots = document.querySelectorAll('.dot');
const totalSlides = slides.length;

function showSlide(index) {
    if (index >= totalSlides) {
        currentSlideIndex = 0;
    } else if (index < 0) {
        currentSlideIndex = totalSlides - 1;
    } else {
        currentSlideIndex = index;
    }
    
    document.querySelector('.carousel-wrapper').style.transform = `translateX(-${currentSlideIndex * 100}%)`;
    dots.forEach((dot, i) => {
        dot.classList.remove('active');
        if (i === currentSlideIndex) {
            dot.classList.add('active');
        }
    });
}

document.getElementById('prevButton').addEventListener('click', () => {
    showSlide(currentSlideIndex - 1);
});

document.getElementById('nextButton').addEventListener('click', () => {
    showSlide(currentSlideIndex + 1);
});

dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        showSlide(index);
    });
});

// Initialize the carousel
showSlide(currentSlideIndex);

