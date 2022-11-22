/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./**/templates/**/*.{html,js}"
  ],
  theme: {
    extend: {
      colors: {
        beige: "#efecd7",
        graphite: "#152934",
        red: "#c21d2e",
      },
    },
  },
  plugins: [],
}
