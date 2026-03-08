document.addEventListener("DOMContentLoaded", () => {
  const homeSong = document.getElementById("homeSong");
  const musicFallbackBtn = document.getElementById("musicFallbackBtn");

  if (homeSong) {
    const targetVolume = 0.2;
    const fadeStep = 0.02;
    const fadeIntervalMs = 120;
    let fadeIntervalId = null;

    homeSong.autoplay = true;
    homeSong.volume = 0;

    const setFallbackVisibility = (isVisible) => {
      if (!musicFallbackBtn) return;
      musicFallbackBtn.hidden = !isVisible;
      musicFallbackBtn.setAttribute("aria-hidden", String(!isVisible));
    };

    const fadeInHomeSong = () => {
      if (fadeIntervalId) {
        clearInterval(fadeIntervalId);
      }

      homeSong.volume = 0;
      fadeIntervalId = setInterval(() => {
        const nextVolume = Math.min(targetVolume, homeSong.volume + fadeStep);
        homeSong.volume = nextVolume;

        if (nextVolume >= targetVolume) {
          clearInterval(fadeIntervalId);
          fadeIntervalId = null;
        }
      }, fadeIntervalMs);
    };

    const playHomeSong = () => {
      if (!homeSong.paused) {
        setFallbackVisibility(false);
        if (homeSong.volume < targetVolume) {
          fadeInHomeSong();
        }
        return;
      }

      homeSong.volume = 0;
      homeSong
        .play()
        .then(() => {
          setFallbackVisibility(false);
          fadeInHomeSong();
        })
        .catch((error) => {
          if (error && error.name === "NotAllowedError") {
            setFallbackVisibility(true);
          }
        });
    };

    playHomeSong();
    window.addEventListener("load", playHomeSong, { once: true });

    homeSong.addEventListener("playing", () => {
      setFallbackVisibility(false);
      if (homeSong.volume < targetVolume) {
        fadeInHomeSong();
      }
    });

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
