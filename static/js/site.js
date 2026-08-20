const nav = document.querySelector(".navbar");
const revealItems = document.querySelectorAll(".reveal");
const counters = document.querySelectorAll("[data-counter]");
const root = document.documentElement;
const themeButtons = document.querySelectorAll(".theme-toggle");
const ignitionOverlay = document.querySelector("#ignitionOverlay");
const engineStartButton = document.querySelector("#engineStartButton");

function currentTheme() {
  return root.getAttribute("data-theme") === "dark" ? "dark" : "light";
}

function updateThemeButtons(theme) {
  themeButtons.forEach((button) => {
    const icon = button.querySelector("i");
    button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
    button.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
    if (icon) {
      icon.className = theme === "dark" ? "bi bi-sun" : "bi bi-moon-stars";
    }
  });
}

function setTheme(theme) {
  if (theme === "dark") {
    root.setAttribute("data-theme", "dark");
    root.style.colorScheme = "dark";
  } else {
    root.removeAttribute("data-theme");
    root.style.colorScheme = "light";
  }

  try {
    localStorage.setItem("cloudrideTheme", theme);
  } catch (error) {
    // Storage can be unavailable in private browser modes; the visual toggle still works.
  }

  updateThemeButtons(theme);
}

updateThemeButtons(currentTheme());

themeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setTheme(currentTheme() === "dark" ? "light" : "dark");
  });
});

function finishIgnition() {
  if (ignitionOverlay?.classList.contains("is-complete")) return;

  root.classList.remove("ignition-pending");
  document.body.classList.remove("ignition-locked");
  try {
    sessionStorage.setItem("cloudrideIgnitionComplete", "true");
  } catch (error) {
    // Non-critical: if session storage is unavailable, the site should still reveal.
  }
  if (ignitionOverlay) {
    ignitionOverlay.classList.add("is-complete");
    ignitionOverlay.setAttribute("aria-hidden", "true");
    window.setTimeout(() => ignitionOverlay.remove(), 250);
  }
}

if (ignitionOverlay && root.classList.contains("ignition-pending")) {
  document.body.classList.add("ignition-locked");
  window.setTimeout(() => engineStartButton?.focus({ preventScroll: true }), 120);

  engineStartButton?.addEventListener("click", () => {
    if (ignitionOverlay.classList.contains("is-starting")) return;

    const title = ignitionOverlay.querySelector("#ignitionTitle");
    const hint = ignitionOverlay.querySelector("#ignitionHint");
    ignitionOverlay.classList.add("is-starting");
    engineStartButton.setAttribute("disabled", "disabled");
    if (title) title.textContent = "Engine Started";
    if (hint) hint.textContent = "Accelerating into CloudRide.";

    const prefersReducedMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
    window.setTimeout(finishIgnition, prefersReducedMotion ? 250 : 1700);
    window.setTimeout(finishIgnition, 3000);
  });

  ignitionOverlay.addEventListener("animationend", (event) => {
    if (event.animationName === "ignitionFade") {
      finishIgnition();
    }
  });
} else if (ignitionOverlay) {
  ignitionOverlay.setAttribute("aria-hidden", "true");
  ignitionOverlay.remove();
}

function updateNav() {
  if (!nav) return;
  nav.classList.toggle("navbar-scrolled", window.scrollY > 12);
}

window.addEventListener("scroll", updateNav, { passive: true });
updateNav();

document.querySelectorAll(".navbar .nav-link, .navbar .btn").forEach((link) => {
  link.addEventListener("click", () => {
    const collapse = document.querySelector(".navbar-collapse.show");
    if (collapse && window.bootstrap) {
      window.bootstrap.Collapse.getOrCreateInstance(collapse).hide();
    }
  });
});

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15 }
);

revealItems.forEach((item) => revealObserver.observe(item));

function animateCounter(el) {
  const target = Number(el.dataset.counter || 0);
  const duration = 1200;
  const startedAt = performance.now();

  function tick(now) {
    const progress = Math.min((now - startedAt) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(target * eased).toLocaleString();
    if (progress < 1) requestAnimationFrame(tick);
  }

  requestAnimationFrame(tick);
}

const counterObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.35 }
);

counters.forEach((counter) => counterObserver.observe(counter));
