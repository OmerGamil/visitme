/** @jest-environment jsdom */
const { fireEvent } = require('@testing-library/dom');
require('@testing-library/jest-dom');

beforeAll(() => {
  global.bootstrap = {
    Modal: jest.fn(() => ({
      show: jest.fn(),
      hide: jest.fn(),
    })),
  };
});

describe('rating.js', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <form id="rating-form" data-country-id="1" data-content-type-id="2" data-user-rating="0">
        <div id="hero-star-rating">
          <i class="star" data-value="5"></i>
        </div>
        <input name="csrfmiddlewaretoken" value="fake-token" />
      </form>
      <div id="commentModal"></div>
      <form id="comment-form">
        <input type="hidden" id="modal-object-id" />
        <input type="hidden" id="modal-content-type-id" />
        <input type="hidden" id="modal-stars" />
      </form>
      <div id="modal-star-display"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        redirected: false,
        json: () => Promise.resolve({ success: true, average_rating: 4.5 }),
      })
    );

    require('../../static/js/rating.js');
    document.dispatchEvent(new Event('DOMContentLoaded'));
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('sends rating and opens modal', async () => {
    const star = document.querySelector('.star');
    fireEvent.click(star);

    expect(fetch).toHaveBeenCalledWith('/rate/object/', expect.any(Object));
  });
});
