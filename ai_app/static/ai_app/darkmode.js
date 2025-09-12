// Toggle dark mode
document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("toggle-dark");
    if (toggleBtn) {
        toggleBtn.addEventListener("click", function() {
            document.body.classList.toggle("dark-mode");
            this.textContent = document.body.classList.contains("dark-mode")
                ? "☀️ Light Mode"
                : "🌙 Dark Mode";
        });
    }
});
