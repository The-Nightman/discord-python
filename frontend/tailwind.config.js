/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      backgroundImage: {
        "root-background": "url('/assets/rootBackground.svg')",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
