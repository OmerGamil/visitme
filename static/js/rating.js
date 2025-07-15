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

  // Set initial state
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
        const countryId = ratingForm.dataset.countryId;
        const contentTypeId = ratingForm.dataset.contentTypeId;
        selectedRating = parseInt(star.dataset.value);

        fetch(`/rate/country/${countryId}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrfToken
          },
          body: `stars=${selectedRating}`
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

            if (container === heroStarContainer && modalStars) {
              modalStars.innerHTML = "";
              for (let i = 1; i <= 5; i++) {
                const icon = document.createElement("i");
                icon.classList.add("bi", "fs-5", "me-1", i <= selectedRating ? "bi-star-fill" : "bi-star");
                modalStars.appendChild(icon);
              }
            }

            if (commentForm) {
              // Clean hidden inputs
              const oldInputs = commentForm.querySelectorAll("input[type=hidden]");
              oldInputs.forEach(input => input.remove());

              const objectInput = document.createElement("input");
              objectInput.type = "hidden";
              objectInput.name = "object_id";
              objectInput.value = countryId;
              commentForm.appendChild(objectInput);

              const contentTypeInput = document.createElement("input");
              contentTypeInput.type = "hidden";
              contentTypeInput.name = "content_type_id";
              contentTypeInput.value = contentTypeId;
              commentForm.appendChild(contentTypeInput);

              const starsInput = document.createElement("input");
              starsInput.type = "hidden";
              starsInput.name = "stars";
              starsInput.value = selectedRating;
              commentForm.appendChild(starsInput);
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

  // Hook up both star areas
  if (heroStarContainer) handleStarClick(heroStarContainer, true); // show modal
  if (formStarContainer) handleStarClick(formStarContainer, false); // do not show modal

  // Comment form submission
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