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

document.addEventListener("DOMContentLoaded", function () {
  const section = document.querySelector(".hero-section");
  const layers = section.querySelectorAll(".hero-slider-layer");
  const raw = section.dataset.images;

  let images;
  try {
    images = JSON.parse(raw);
  } catch (e) {
    console.error("Slideshow image parse error:", e);
    return;
  }

  if (!images.length) return;

  let current = 0;
  layers[0].style.backgroundImage = `url('${images[0]}')`;
  layers[0].classList.add("active");

  function preload(src, callback) {
    const img = new Image();
    img.onload = callback;
    img.src = src;
  }

  setInterval(() => {
    const next = (current + 1) % images.length;
    const nextLayer = layers[1 - (current % 2)];
    const activeLayer = layers[current % 2];

    preload(images[next], () => {
      nextLayer.style.backgroundImage = `url('${images[next]}')`;
      nextLayer.classList.add("active");
      activeLayer.classList.remove("active");
      current = next;
    });
  }, 3000);
});