// Shared behaviour for every page. Load this last, after any page-specific
// script that adds cards to the page.

// Navbar border once the page scrolls
const navbar = document.getElementById('navbar');
const updateNavbar = () => navbar.classList.toggle('scrolled', window.scrollY > 50);
window.addEventListener('scroll', updateNavbar, { passive: true });
updateNavbar();

// Stagger cards inside each grid so they reveal one after another
document.querySelectorAll('.grid').forEach((grid) => {
    [...grid.children].forEach((card, i) => {
        card.style.setProperty('--delay', `${Math.min(i, 5) * 0.08}s`);
    });
});

// Reveal .fade-up elements as they scroll into view
const observer = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
);

document.querySelectorAll('.fade-up').forEach((el) => observer.observe(el));

// Footer year
document.querySelectorAll('[data-year]').forEach((el) => {
    el.textContent = new Date().getFullYear();
});
