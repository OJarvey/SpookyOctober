/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './core/templates/**/*.html',
    './*/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'pumpkin': '#FF6600',
        'midnight': '#1a1a1a',
        'spooky-purple': '#6B2D6B',
      },
      fontFamily: {
        'spooky': ['Creepster', 'cursive'],
      },
    },
  },
  plugins: [],
}
