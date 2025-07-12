document.addEventListener('DOMContentLoaded', function () {
  const navbar = document.querySelector('.navbar');

  // Check if page has a hero section
  const hasHero = document.querySelector('.hero-section');

  function handleNavbarScroll() {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }

  // If hero exists, change on scroll
  if (hasHero) {
    window.addEventListener('scroll', handleNavbarScroll);
    handleNavbarScroll(); // run once on load
  } else {
    // No hero section (e.g. Explore page) — force scrolled
    navbar.classList.add('scrolled');
  }
});