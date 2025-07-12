document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".wishlist-btn").forEach(btn => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();

      const icon = this.querySelector("i");
      const contentTypeId = this.dataset.contentType;
      const objectId = this.dataset.objectId;

      fetch("/wishlist/toggle/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: `content_type_id=${contentTypeId}&object_id=${objectId}`
      })
      .then(res => res.json())
      .then(data => {
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
