document.addEventListener("DOMContentLoaded", () => {
  const homeSong = document.getElementById("homeSong");
  const musicFallbackBtn = document.getElementById("musicFallbackBtn");

  if (homeSong) {
    homeSong.autoplay = true;

    const setFallbackVisibility = (isVisible) => {
      if (!musicFallbackBtn) return;
      musicFallbackBtn.hidden = !isVisible;
      musicFallbackBtn.setAttribute("aria-hidden", String(!isVisible));
    };

    const playHomeSong = () => {
      homeSong
        .play()
        .then(() => {
          setFallbackVisibility(false);
        })
        .catch((error) => {
          if (error && error.name === "NotAllowedError") {
            setFallbackVisibility(true);
          }
        });
    };

    playHomeSong();
    window.addEventListener("load", playHomeSong, { once: true });

    homeSong.addEventListener("playing", () => setFallbackVisibility(false));

    if (musicFallbackBtn) {
      musicFallbackBtn.addEventListener("click", playHomeSong);
    }
  }

  const revealElements = document.querySelectorAll(".reveal-up");

  if (!revealElements.length) return;

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
