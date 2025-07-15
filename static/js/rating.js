document.addEventListener("DOMContentLoaded", () => {
  const ratingForm = document.getElementById("rating-form");
  if (!ratingForm) return;

  const ratingValue = document.getElementById("rating-value");
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const commentModalElement = document.getElementById("commentModal");
  const modalStars = document.getElementById("modal-star-display");
  const commentForm = document.getElementById("comment-form");

  const heroStarContainer = document.getElementById("hero-star-rating");
  const formStarContainer = document.getElementById("form-star-rating");

  let commentModal = null;
  if (commentModalElement) {
    commentModal = new bootstrap.Modal(commentModalElement);
  }

  let selectedRating = parseFloat(ratingForm.dataset.userRating || "0");

  function fillStars(container, upTo) {
    const stars = container.querySelectorAll(".star");
    stars.forEach(star => {
      const value = parseInt(star.dataset.value);
      star.classList.remove("bi-star", "bi-star-fill");
      star.classList.add(value <= upTo ? "bi-star-fill" : "bi-star");
    });
  }

  // Initial fill
  if (heroStarContainer) fillStars(heroStarContainer, selectedRating);
  if (formStarContainer) fillStars(formStarContainer, selectedRating);

  function handleStarClick(container, showModal = true) {
    const stars = container.querySelectorAll(".star");

    stars.forEach(star => {
      star.addEventListener("mouseenter", () => {
        fillStars(container, parseInt(star.dataset.value));
      });

      star.addEventListener("mouseleave", () => {
        fillStars(container, selectedRating);
      });

      star.addEventListener("click", () => {
        const objectId = ratingForm.dataset.countryId;
        const contentTypeId = ratingForm.dataset.contentTypeId;
        selectedRating = parseInt(star.dataset.value);

        fetch("/rate/object/", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrfToken
          },
          body: `stars=${selectedRating}&object_id=${objectId}&content_type_id=${contentTypeId}`
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
          if (data && data.success) {
            if (ratingValue) ratingValue.textContent = data.average_rating;
            fillStars(container, selectedRating);

            // Inject star visuals into modal
            if (container === heroStarContainer && modalStars) {
              modalStars.innerHTML = "";
              for (let i = 1; i <= 5; i++) {
                const icon = document.createElement("i");
                icon.classList.add("bi", "fs-5", "me-1", i <= selectedRating ? "bi-star-fill" : "bi-star");
                modalStars.appendChild(icon);
              }
            }

            // Update fallback hidden inputs in modal
            if (commentForm) {
              const objectInput = document.getElementById("modal-object-id");
              const contentTypeInput = document.getElementById("modal-content-type-id");
              const starsInput = document.getElementById("modal-stars");

              if (objectInput) objectInput.value = objectId;
              if (contentTypeInput) contentTypeInput.value = contentTypeId;
              if (starsInput) starsInput.value = selectedRating;
            }

            if (showModal && commentModal) {
              commentModal.show();
            }
          } else {
            alert("Failed to rate.");
          }
        });
      });
    });
  }

  // Hook up star interactions
  if (heroStarContainer) handleStarClick(heroStarContainer, true);  // hero -> triggers modal
  if (formStarContainer) handleStarClick(formStarContainer, false); // form -> no modal

  // Handle comment submission
  if (commentForm) {
    commentForm.addEventListener("submit", function (e) {
      e.preventDefault();

      const formData = new FormData(this);

      fetch("/rate/comment/", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken
        },
        body: formData
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          if (commentModal) commentModal.hide();
          setTimeout(() => document.body.focus(), 300);
          alert("Thanks for your comment!");
        } else {
          alert("Failed to save comment: " + (data.error || ""));
        }
      });
    });
  }
});
