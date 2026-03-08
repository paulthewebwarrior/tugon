document.addEventListener("DOMContentLoaded", () => {
  // Theme toggle functionality
  const themeToggle = document.getElementById("themeToggle");
  const html = document.documentElement;

  // Load saved theme preference or default to light mode
  const savedTheme = localStorage.getItem("theme") || "light";
  html.setAttribute("data-theme", savedTheme);
  updateThemeToggleIcon(savedTheme);

  // Theme toggle click handler
  themeToggle.addEventListener("click", () => {
    const currentTheme = html.getAttribute("data-theme");
    const newTheme = currentTheme === "light" ? "dark" : "light";

    html.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    updateThemeToggleIcon(newTheme);
  });

  // Update toggle button icon based on current theme
  function updateThemeToggleIcon(theme) {
    if (theme === "dark") {
      themeToggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
      themeToggle.title = "Switch to light mode";
    } else {
      themeToggle.innerHTML = '<i class="bi bi-moon-fill"></i>';
      themeToggle.title = "Switch to dark mode";
    }
  }

  // Scroll reveal animation
  const revealElements = document.querySelectorAll(".reveal-up");

  if (!revealElements.length) {
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.15,
      rootMargin: "0px 0px -40px 0px",
    }
  );

  revealElements.forEach((element) => observer.observe(element));
});