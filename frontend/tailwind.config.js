/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,scss}",
  ],
  theme: {
    extend: {
      colors: {
        'convertio-red': '#f74040',
        'convertio-red-darker': '#e03434',
        'header-gray': '#4a4a4a',
        'dark-charcoal': '#333333',
      }
    },
  },
  plugins: [],
}