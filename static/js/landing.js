(() => {
  const root = document.documentElement;
  const themeButton = document.getElementById('theme');
  const sizeButtons = document.querySelectorAll('[data-size]');
  const scales = { small: 0.75, medium: 1, large: 1.25 };

  function setTheme(value) {
    const theme = value === 'dark' ? 'dark' : 'light';
    root.dataset.theme = theme;
    if (themeButton) {
      themeButton.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
      themeButton.setAttribute('aria-pressed', String(theme === 'dark'));
    }
    try { localStorage.setItem('mb-theme', theme); } catch (_) { /* optional preference */ }
  }

  function setSize(value) {
    const size = Object.hasOwn(scales, value) ? value : 'medium';
    root.style.setProperty('--scale', String(scales[size]));
    sizeButtons.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.size === size)));
    try { localStorage.setItem('mb-size', size); } catch (_) { /* optional preference */ }
  }

  let theme = 'light';
  let size = 'medium';
  try {
    theme = localStorage.getItem('mb-theme') || 'light';
    size = localStorage.getItem('mb-size') || 'medium';
  } catch (_) { /* Keep defaults. */ }
  setTheme(theme);
  setSize(size);
  themeButton?.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'));
  sizeButtons.forEach((button) => button.addEventListener('click', () => setSize(button.dataset.size)));
})();
