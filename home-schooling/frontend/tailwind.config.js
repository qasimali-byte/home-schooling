/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      visibility: ["group-hover"],
      colors: {
        "primary": "var(--primary)",
        "secondary": "var(--secondary)",
        "btn-primary":"var(--btn-primary)"
      },
    },
  },
  plugins: [],
}

