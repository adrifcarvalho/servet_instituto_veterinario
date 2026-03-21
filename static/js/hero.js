let currentSlide = 0;
const slides = document.querySelectorAll('.slide-img');
const totalSlides = slides.length;

setInterval(() => {
    slides[currentSlide].classList.remove('active');
    currentSlide = (currentSlide + 1) % totalSlides;
    slides[currentSlide].classList.add('active');
}, 4000);

// Ajusta altura do slider igual à coluna do texto
function adjustSliderHeight() {
    const heroText = document.querySelector('.hero-text');
    const sliderContainer = document.querySelector('.hero-slider-container');

    if(window.innerWidth < 992){
        const height = heroText.offsetHeight;
        sliderContainer.style.height = height + "px";
        sliderContainer.style.marginTop = "20px";
    } else {
        sliderContainer.style.height = "100%";
        sliderContainer.style.marginTop = "0";
    }
}

window.addEventListener('load', adjustSliderHeight);
window.addEventListener('resize', adjustSliderHeight);
