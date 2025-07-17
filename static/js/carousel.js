document.addEventListener("DOMContentLoaded", () => {
  const carousels = document.querySelectorAll(".swiper");
  carousels.forEach((carousel) => {
    new Swiper(carousel, {
      slidesPerView: 1,
      spaceBetween: 20,
      loop: false,
      navigation: {
        nextEl: carousel.querySelector(".swiper-button-next"),
        prevEl: carousel.querySelector(".swiper-button-prev")
      },
      breakpoints: {
        768: {
          slidesPerView: 2
        },
        992: {
          slidesPerView: 3
        }
      }
    });
  });
});
