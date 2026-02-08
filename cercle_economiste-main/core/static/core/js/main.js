
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) { window.lucide.createIcons(); }
    
    // Mobile Menu (toggle)
    const btn = document.getElementById('mobile-menu-btn');
    const menu = document.getElementById('mobile-menu');
    if (btn && menu) btn.addEventListener('click', () => menu.classList.toggle('hidden'));

    // Carousel Logic
    const track = document.getElementById('carousel-track');
    if (track) {
        const slides = track.children;
        let index = 0;
        const total = slides.length;
        
        const updateSlide = () => {
            track.style.transform = `translateX(-${index * 100}%)`;
            document.querySelectorAll('.dot-indicator').forEach((dot, i) => {
                dot.style.backgroundColor = i === index ? '#c25e3d' : '#e5e7eb';
                dot.style.width = i === index ? '24px' : '8px';
            });
        };

        window.nextSlide = () => { index = (index + 1) % total; updateSlide(); };
        window.prevSlide = () => { index = (index - 1 + total) % total; updateSlide(); };
        window.goToSlide = (i) => { index = i; updateSlide(); };

        setInterval(window.nextSlide, 6000);
    }
});
