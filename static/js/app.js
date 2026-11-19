(() => {
  const root = document.documentElement;
  const themeKey = 'mb-theme';
  const sizeKey = 'mb-size';
  const sizeScale = { small: 0.75, medium: 1, large: 1.25 };

  function setTheme(value) {
    const theme = value === 'dark' ? 'dark' : 'light';
    root.dataset.theme = theme;
    try { localStorage.setItem(themeKey, theme); } catch (_) { /* Storage may be unavailable. */ }
    document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
      button.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
      button.setAttribute('aria-pressed', String(theme === 'dark'));
    });
  }

  function setSize(value) {
    const size = Object.hasOwn(sizeScale, value) ? value : 'medium';
    root.style.setProperty('--scale', String(sizeScale[size]));
    try { localStorage.setItem(sizeKey, size); } catch (_) { /* Storage may be unavailable. */ }
    document.querySelectorAll('[data-size]').forEach((button) => {
      button.setAttribute('aria-pressed', String(button.dataset.size === size));
    });
  }

  let savedTheme = 'light';
  let savedSize = 'medium';
  try {
    savedTheme = localStorage.getItem(themeKey) || 'light';
    savedSize = localStorage.getItem(sizeKey) || 'medium';
  } catch (_) { /* Use accessible defaults when storage is unavailable. */ }
  setTheme(savedTheme);
  setSize(savedSize);

  document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
    button.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'));
  });
  document.querySelectorAll('[data-size]').forEach((button) => {
    button.addEventListener('click', () => setSize(button.dataset.size));
  });
})();
