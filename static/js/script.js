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

  // ✅ Preserve active Bootstrap tab after refresh
  const triggerTabList = [].slice.call(document.querySelectorAll('#countryTab button'));
  triggerTabList.forEach(function (triggerEl) {
    const tabTrigger = new bootstrap.Tab(triggerEl);

    triggerEl.addEventListener('click', function (event) {
      event.preventDefault();
      tabTrigger.show();
      const hash = triggerEl.getAttribute('data-bs-target');
      if (history.replaceState) {
        history.replaceState(null, null, hash);
      } else {
        window.location.hash = hash;
      }
    });
  });

  const hash = window.location.hash;
  if (hash) {
    const tabTrigger = new bootstrap.Tab(document.querySelector(`#countryTab button[data-bs-target="${hash}"]`));
    if (tabTrigger) {
      tabTrigger.show();
    }
  }
});
