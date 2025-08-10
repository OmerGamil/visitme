document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".wishlist-btn").forEach(btn => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();

      const icon = this.querySelector("i");
      const contentTypeId = this.dataset.contentType;
      const objectId = this.dataset.objectId;

      const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
      const csrfToken = csrfInput ? csrfInput.value : document.querySelector('meta[name="csrf-token"]').getAttribute("content");

      fetch("/wishlist/toggle/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrfToken
        },
        body: `content_type_id=${contentTypeId}&object_id=${objectId}`
      })
      .then(res => {
        if (res.redirected && res.url.includes("/accounts/login")) {
          alert("You're not logged in.");
          window.location.href = `/accounts/login/?next=${encodeURIComponent(window.location.pathname)}`;
          return;
        }
        return res.json();
      })
      .then(data => {
        if (!data) return;

        if (data.status === "added") {
          icon.classList.remove("bi-heart");
          icon.classList.add("bi-heart-fill", "text-danger");
        } else {
          icon.classList.add("bi-heart");
          icon.classList.remove("bi-heart-fill", "text-danger");
        }
      });
    });
  });
});
