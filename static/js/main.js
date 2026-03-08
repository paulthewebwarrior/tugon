document.addEventListener("DOMContentLoaded", () => {
  const homeSong = document.getElementById("homeSong");

  if (homeSong) {
    homeSong.autoplay = true;

    const playHomeSong = () => {
      homeSong.play().catch(() => {
        // Ignore errors when playback is blocked or no source file exists.
      });
    };

    playHomeSong();
    window.addEventListener("load", playHomeSong, { once: true });

    const unlockAudio = () => {
      playHomeSong();
      document.removeEventListener("click", unlockAudio);
      document.removeEventListener("keydown", unlockAudio);
      document.removeEventListener("touchstart", unlockAudio);
    };

    document.addEventListener("click", unlockAudio, { once: true });
    document.addEventListener("keydown", unlockAudio, { once: true });
    document.addEventListener("touchstart", unlockAudio, { once: true });
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
