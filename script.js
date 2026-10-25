document.addEventListener("DOMContentLoaded", () => {
  // Delete confirmation
  document.querySelectorAll(".delete-form").forEach((form) => {
    form.addEventListener("submit", (e) => {
      const confirmed = confirm("Delete this entry? This can't be undone.");
      if (!confirmed) {
        e.preventDefault();
      }
    });
  });

  // Login / Sign up tab toggle
  const tabButtons = document.querySelectorAll(".tab-btn");
  const formAction = document.getElementById("form-action");
  const submitBtn = document.getElementById("submit-btn");
  const hintText = document.getElementById("hint-text");

  tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      tabButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      const tab = btn.dataset.tab;
      if (formAction) formAction.value = tab;

      if (tab === "signup") {
        if (submitBtn) submitBtn.textContent = "Create account";
        if (hintText) hintText.textContent = "Already have an account? Click Login above.";
      } else {
        if (submitBtn) submitBtn.textContent = "Login";
        if (hintText) hintText.textContent = "New here? Click Sign up above to create your own private journal.";
      }
    });
  });
});