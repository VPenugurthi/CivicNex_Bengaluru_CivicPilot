/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'city-blue': '#0F172A',
        'city-accent': '#3B82F6',
        'city-success': '#10B981',
        'city-warning': '#F59E0B',
        'city-danger': '#EF4444',
        'city-bg': '#F8FAFC',
      },
    },
  },
  plugins: [],
}
