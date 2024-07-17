/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: ["./templates/**/*.{html,htm}", "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {},
  },
  plugins: [require("flowbite/plugin")],
}

