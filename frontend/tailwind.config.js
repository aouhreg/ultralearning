/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#6366f1', hover: '#4f46e5' },
        surface: { DEFAULT: '#1e1e2e', card: '#27273a', border: '#3d3d5c' }
      },
      fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] }
    }
  },
  plugins: []
}
