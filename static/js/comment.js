document.addEventListener("DOMContentLoaded", () => {
  const commentForm = document.getElementById("user-comment-form");
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  if (!commentForm) return;

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
        alert(data.created ? "Thanks for your review!" : "Review updated!");
        // ✅ Refresh the page to reflect the update
        window.location.reload();
      } else {
        alert("Error: " + (data.error || "Could not submit review"));
      }
    })
    .catch(err => {
      console.error("AJAX error:", err);
      alert("Unexpected error occurred.");
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const editBtn = document.getElementById("edit-comment-btn");
  const cancelBtn = document.getElementById("cancel-edit");
  const form = document.getElementById("user-comment-form");
  const display = document.getElementById("comment-display");

  if (editBtn) {
    editBtn.addEventListener("click", () => {
      form.style.display = "block";
      display.style.display = "none";
    });
  }

  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      form.style.display = "none";
      display.style.display = "block";
    });
  }
});
