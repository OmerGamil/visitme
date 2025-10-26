/** @jest-environment jsdom */
const { fireEvent } = require('@testing-library/dom');
require('@testing-library/jest-dom');

describe('script.js', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div class="navbar"></div>
      <div class="hero-section"></div>
      <div id="countryTab">
        <button data-bs-target="#tab1">Tab 1</button>
      </div>
    `;

    global.bootstrap = {
      Tab: function () {
        return { show: jest.fn() };
      }
    };

    require('../../static/js/script.js');
    document.dispatchEvent(new Event('DOMContentLoaded'));
    window.scrollY = 100;
    fireEvent.scroll(window);
  });

  test('adds scrolled class on navbar scroll', () => {
    const navbar = document.querySelector('.navbar');
    expect(navbar.classList.contains('scrolled')).toBe(true);
  });
});
