document.addEventListener("DOMContentLoaded", () => {
  const homeSong = document.getElementById("homeSong");
  const musicControlBtn = document.getElementById("musicControlBtn");

  if (homeSong) {
    const targetVolume = 0.2;
    const fadeStep = 0.02;
    const fadeIntervalMs = 120;
    let fadeIntervalId = null;

    homeSong.autoplay = true;
    homeSong.volume = 0;

    const setControlVisibility = (isVisible) => {
      if (!musicControlBtn) return;
      musicControlBtn.hidden = !isVisible;
      musicControlBtn.setAttribute("aria-hidden", String(!isVisible));
    };

    const setControlState = (isPlaying) => {
      if (!musicControlBtn) return;

      const controlIcon = musicControlBtn.querySelector("i");
      const controlLabel = musicControlBtn.querySelector("span");

      musicControlBtn.setAttribute("aria-pressed", String(isPlaying));

      if (controlIcon) {
        controlIcon.classList.remove("bi-play-fill", "bi-pause-fill");
        controlIcon.classList.add(isPlaying ? "bi-pause-fill" : "bi-play-fill");
      }

      if (controlLabel) {
        controlLabel.textContent = isPlaying ? "Pause Music" : "Play Music";
      }
    };

    const stopFade = () => {
      if (!fadeIntervalId) return;
      clearInterval(fadeIntervalId);
      fadeIntervalId = null;
    };

    const fadeInHomeSong = () => {
      stopFade();

      homeSong.volume = 0;
      fadeIntervalId = setInterval(() => {
        const nextVolume = Math.min(targetVolume, homeSong.volume + fadeStep);
        homeSong.volume = nextVolume;

        if (nextVolume >= targetVolume) {
          stopFade();
        }
      }, fadeIntervalMs);
    };

    const playHomeSong = () => {
      if (!homeSong.paused) {
        setControlVisibility(true);
        setControlState(true);
        if (homeSong.volume < targetVolume) {
          fadeInHomeSong();
        }
        return;
      }

      homeSong.volume = 0;
      homeSong
        .play()
        .then(() => {
          setControlVisibility(true);
          setControlState(true);
          fadeInHomeSong();
        })
        .catch((error) => {
          if (error && error.name === "NotAllowedError") {
            setControlVisibility(true);
            setControlState(false);
          }
        });
    };

    const pauseHomeSong = () => {
      if (homeSong.paused) {
        setControlState(false);
        return;
      }

      stopFade();
      homeSong.pause();
      setControlState(false);
    };

    const toggleHomeSong = () => {
      if (homeSong.paused) {
        playHomeSong();
      } else {
        pauseHomeSong();
      }
    };

    setControlVisibility(true);
    setControlState(false);

    playHomeSong();
    window.addEventListener("load", playHomeSong, { once: true });

    homeSong.addEventListener("playing", () => {
      setControlVisibility(true);
      setControlState(true);
      if (homeSong.volume < targetVolume) {
        fadeInHomeSong();
      }
    });

    homeSong.addEventListener("pause", () => {
      setControlState(false);
    });

    if (musicControlBtn) {
      musicControlBtn.addEventListener("click", toggleHomeSong);
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
