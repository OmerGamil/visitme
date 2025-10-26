/** @jest-environment jsdom */
require('@testing-library/jest-dom');

describe('carousel.js', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div class="swiper">
        <div class="swiper-button-next"></div>
        <div class="swiper-button-prev"></div>
      </div>
    `;

    global.Swiper = jest.fn();
    require('../../static/js/carousel.js');
    document.dispatchEvent(new Event('DOMContentLoaded'));
  });

  test('initializes Swiper on .swiper elements', () => {
    expect(global.Swiper).toHaveBeenCalled();
  });
});
