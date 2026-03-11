/**
 * Tugon Main Application Entry Point
 */

// Page transition loader
const pageLoader = document.getElementById('page-loader');

function showTransition() {
  pageLoader.classList.add('active');
  pageLoader.style.display = 'flex';
  
  setTimeout(() => {
    pageLoader.classList.remove('active');
    setTimeout(() => {
      pageLoader.style.display = 'none';
    }, 300);
  }, 2000);
}

// Show transition on any internal link click except council pages
document.addEventListener('click', (e) => {
  const link = e.target.closest('a');
  if (!link) return;
  
  const href = link.getAttribute('href');
  if (!href) return;
  
  // Skip external links, anchors, and special links
  if (href.startsWith('mailto:') || 
      href.startsWith('tel:') || 
      href.startsWith('http') && !href.includes(window.location.hostname) ||
      href.startsWith('#') ||
      link.getAttribute('data-bs-toggle') === 'dropdown') {
    return;
  }
  
  // Skip council page links (keep transition for main nav only)
  if (href.includes('/council/')) {
    return;
  }
  
  showTransition();
});

// Always show transition on page load (2 seconds)
window.addEventListener('load', () => {
  setTimeout(() => {
    showTransition();
  }, 100);
});

// Handle browser back/forward buttons
window.addEventListener('pageshow', () => {
  setTimeout(() => {
    showTransition();
  }, 100);
});

document.addEventListener("DOMContentLoaded", () => {
  // Election countdown
  const countdownElement = document.getElementById("electionCountdown");

  if (countdownElement) {
    const electionDate = countdownElement.getAttribute("data-election-date");

    if (electionDate) {
      const dayNode = countdownElement.querySelector('[data-unit="days"]');
      const hourNode = countdownElement.querySelector('[data-unit="hours"]');
      const minuteNode = countdownElement.querySelector('[data-unit="minutes"]');

      const updateCountdown = () => {
        const now = new Date();
        const target = new Date(`${electionDate}T00:00:00`);
        const diff = target.getTime() - now.getTime();

        if (diff <= 0) {
          if (dayNode) dayNode.textContent = "0";
          if (hourNode) hourNode.textContent = "0";
          if (minuteNode) minuteNode.textContent = "0";
          return;
        }

        const totalMinutes = Math.floor(diff / (1000 * 60));
        const days = Math.floor(totalMinutes / (60 * 24));
        const hours = Math.floor((totalMinutes % (60 * 24)) / 60);
        const minutes = totalMinutes % 60;

        if (dayNode) dayNode.textContent = String(days);
        if (hourNode) hourNode.textContent = String(hours);
        if (minuteNode) minuteNode.textContent = String(minutes);
      };

      updateCountdown();
      setInterval(updateCountdown, 30000);
    }
  }

  // Initial reveal animations for static content
  const revealElements = document.querySelectorAll(".reveal-up");

  if (revealElements.length) {
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
  }

  // Initialize page-specific JavaScript
  if (typeof Pages !== 'undefined') {
    Pages.init();
  }
});
