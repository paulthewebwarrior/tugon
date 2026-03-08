document.addEventListener("DOMContentLoaded", () => {
  const homeSong = document.getElementById("homeSong");
  const musicPlayBtn = document.getElementById("musicPlayBtn");
  const musicPauseBtn = document.getElementById("musicPauseBtn");

  if (homeSong) {
    const targetVolume = 0.2;
    const fadeStep = 0.02;
    const fadeIntervalMs = 120;
    let fadeIntervalId = null;

    homeSong.autoplay = true;
    homeSong.volume = 0;

    const setControlState = (isPlaying) => {
      if (musicPlayBtn) {
        musicPlayBtn.disabled = isPlaying;
      }

      if (musicPauseBtn) {
        musicPauseBtn.disabled = !isPlaying;
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
          setControlState(true);
          fadeInHomeSong();
        })
        .catch((error) => {
          if (error && error.name === "NotAllowedError") {
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

    setControlState(false);

    playHomeSong();
    window.addEventListener("load", playHomeSong, { once: true });

    homeSong.addEventListener("playing", () => {
      setControlState(true);
      if (homeSong.volume < targetVolume) {
        fadeInHomeSong();
      }
    });

    homeSong.addEventListener("pause", () => {
      setControlState(false);
    });

    if (musicPlayBtn) {
      musicPlayBtn.addEventListener("click", playHomeSong);
    }

    if (musicPauseBtn) {
      musicPauseBtn.addEventListener("click", pauseHomeSong);
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
