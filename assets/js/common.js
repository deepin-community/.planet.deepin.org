const setColorTheme = (theme) => {
  document.documentElement.setAttribute('data-bs-theme', theme);
  window.localStorage.setItem('colorScheme', theme);
}

const colorScheme = window.localStorage.getItem("colorScheme");
if (colorScheme) {
  setColorTheme(colorScheme);
}

const storeLang = (event) => {
  window.localStorage.setItem('lang', event.target.lang);
}