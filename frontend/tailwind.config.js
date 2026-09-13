/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: false,

  theme: {
    extend: {
      colors: {
        // Primary color scale (blue-600 based)
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6', // Primary color - main blue
          600: '#2563eb', // Main primary
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
        // Secondary color scale (indigo-600 based)
        secondary: {
          50: '#eef4ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5', // Main secondary
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
          950: '#1e1b4b',
        },
        // Semantic colors
        semantic: {
          success: {
            50: '#f0fdf4', 100: '#dcfce7', 200: '#bbf7d0', 300: '#86efac',
            400: '#4ade80', 500: '#22c55e', 600: '#16a34a', 700: '#15803d',
            800: '#166534', 900: '#14532d', 950: '#052e16',
          },
          warning: {
            50: '#fffbeb', 100: '#fef3c7', 200: '#fde68a', 300: '#fcd34d',
            400: '#fbbf24', 500: '#f59e0b', 600: '#d97706', 700: '#b45309',
            800: '#92400e', 900: '#78350f', 950: '#271803',
          },
          error: {
            50: '#fef2f2', 100: '#fee2e2', 200: '#fecaca', 300: '#fca5a5',
            400: '#f87171', 500: '#ef4444', 600: '#dc2626', 700: '#b91c1c',
            800: '#991b1b', 900: '#7f1d1d', 950: '#3f0101',
          },
          info: {
            50: '#eff6ff', 100: '#dbeafe', 200: '#bfdbfe', 300: '#93c5fd',
            400: '#60a5fa', 500: '#3b82f6', 600: '#2563eb', 700: '#1d4ed8',
            800: '#1e40af', 900: '#1e3a8a', 950: '#172554',
          },
        },
        // Neutral scale
        neutral: {
          50: '#fafafa', 100: '#f4f4f5', 200: '#e4e4e7', 300: '#d4d4d8',
          400: '#a1a1aa', 500: '#71717a', 600: '#52525b', 700: '#404042',
          800: '#27272a', 900: '#18181b', 950: '#09090b',
        },
      },
      
      // Typography - Inter font with responsive clamp() sizing
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },

      fontSize: {
        // H1 - Large headings and page titles (3.2rem - 4.5rem responsive)
        'h-1': ['clamp(3.2rem, 1vw + 2.6rem, 4.5rem)', '700', '#0f172a'], // ~51.2px - 72px
        // H2 - Section headings (2.5rem - 3.2rem)
        'h-2': ['clamp(2.5rem, 0.7vw + 1.9rem, 3.2rem)', '600', '#1e293b'], // ~40px - 51.2px
        // H3 - Card/panel headings (1.8rem - 2.2rem)
        'h-3': ['clamp(1.8rem, 0.4vw + 1.6rem, 2.2rem)', '600', '#334155'], // ~28.8px - 35.2px
      },

      spacing: {
        // Spacing scale with wider gaps (84 = 21rem for expanded layouts)
        '84': '21rem',    // Wide gap for large content areas
        '96': '24rem',    // Extra wide
        '075': '3rem',    // 3/4 inch
      },

      boxShadow: {
        // Card shadow - subtle elevation for cards, tables, modals
        'card-sm': '0px 1px 2px 0px rgba(0, 0, 0, 0.05), 0px 1px 3px 1px rgba(0, 0, 0, 0.03)',
        'card': '0px 4px 6px -1px rgba(0, 0, 0, 0.1), 0px 2px 4px -2px rgba(0, 0, 0, 0.1)', // Medium elevation
        'card-lg': '0px 10px 15px -3px rgba(0, 0, 0, 0.1), 0px 4px 6px -2px rgba(0, 0, 0, 0.05)', // Large elevation
        'modal-sm': '0px 4px 12px rgba(0, 0, 0, 0.07), 0px 0px 8px rgba(0, 0, 0, 0.03)',
        'modal': '0px 25px 50px -12px rgba(0, 0, 0, 0.25)', // Modal with blur effect
        'dropdown': '0px 4px 12px rgba(0, 0, 0, 0.15), 0px 0px 8px rgba(0, 0, 0, 0.1)',
      },
    },
  },
  plugins: [],
}
