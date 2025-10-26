/** @jest-environment jsdom */
const { fireEvent } = require("@testing-library/dom");
require("@testing-library/jest-dom");

describe("wishlist.js", () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <button class="wishlist-btn" data-content-type="1" data-object-id="123">
        <i class="bi bi-heart"></i>
      </button>
      <meta name="csrf-token" content="fake-token">
    `;

    global.alert = jest.fn();

    global.fetch = jest.fn(() =>
      Promise.resolve({
        redirected: false,
        json: () => Promise.resolve({ status: "added" }),
      })
    );

    jest.isolateModules(() => {
      require("../../static/js/wishlist.js");
    });
    document.dispatchEvent(new Event("DOMContentLoaded"));
  });

  afterEach(() => {
    jest.clearAllMocks();
    delete window.__TEST_REDIRECT__;
  });

  test("adds item to wishlist", async () => {
    const btn = document.querySelector(".wishlist-btn");
    fireEvent.click(btn);
    expect(fetch).toHaveBeenCalledWith("/wishlist/toggle/", expect.any(Object));
  });

  test("redirects if not logged in", async () => {
    fetch.mockImplementationOnce(() =>
      Promise.resolve({
        redirected: true,
        url: "/accounts/login/",
      })
    );

    const btn = document.querySelector(".wishlist-btn");
    fireEvent.click(btn);

    await new Promise((r) => setTimeout(r, 0));

    expect(alert).toHaveBeenCalledWith("You're not logged in.");
    // ✅ Check the non-navigating test hook instead of window.location.href
    expect(window.__TEST_REDIRECT__).toContain("/accounts/login");
  });
});
