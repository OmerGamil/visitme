/** @jest-environment jsdom */
const { fireEvent } = require('@testing-library/dom');
require('@testing-library/jest-dom');

describe('comment.js', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <form id="user-comment-form">
        <textarea name="text">Hello</textarea>
        <button type="submit">Submit</button>
      </form>
      <input type="hidden" name="csrfmiddlewaretoken" value="fake-token" />
      <div id="comment-display" style="display: none;"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ success: true, created: true }),
      })
    );

    global.alert = jest.fn();
    global.window.location = { reload: jest.fn() };

    require('../../static/js/comment.js');
    document.dispatchEvent(new Event('DOMContentLoaded'));
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('submits the comment form via AJAX', async () => {
    const form = document.getElementById('user-comment-form');
    fireEvent.submit(form);

    expect(fetch).toHaveBeenCalledWith('/rate/comment/', expect.any(Object));
  });
});
