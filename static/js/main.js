/**
 * Tugon Main Application Entry Point
 */

// Page loading screen
(function() {
  const pageLoader = document.getElementById('page-loader');
  
  if (!pageLoader) {
    console.log('Page loader not found');
    return;
  }

  function showLoader() {
    pageLoader.classList.add('active');
    pageLoader.style.display = 'flex';
    console.log('Loader shown');
  }

  function hideLoader() {
    pageLoader.classList.remove('active');
    pageLoader.style.display = 'none';
    console.log('Loader hidden');
  }

  // Show loader on link click
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (!link) return;
    
    const href = link.getAttribute('href');
    if (!href) return;
    
    // Skip external links, anchors, and special links
    if (href.startsWith('mailto:') || 
        href.startsWith('tel:') || 
        (href.startsWith('http') && !href.includes(window.location.hostname)) ||
        href.startsWith('#') ||
        link.getAttribute('data-bs-toggle') === 'dropdown') {
      return;
    }
    
    // Skip council page links
    if (href.includes('/council/')) {
      return;
    }
    
    showLoader();
  });

  // Hide loader when page loads
  window.addEventListener('load', () => {
    setTimeout(hideLoader, 100);
  });

  // Handle browser back/forward buttons
  window.addEventListener('pageshow', () => {
    setTimeout(hideLoader, 100);
  });

  // Force hide after 2 seconds as fallback
  setTimeout(hideLoader, 2000);
})();

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
