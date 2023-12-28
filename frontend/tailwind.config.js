import { fontFamily } from "tailwindcss/defaultTheme";

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    fontFamily: {
      sans: ["var(--font-sans)", ...fontFamily.sans],
      display: ["var(--font-display)", ...fontFamily.sans],
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "#6D9773",
          foreground: "#6D9773",
        },
        secondary: {
          DEFAULT: "#0C3B2E",
          foreground: "#0C3B2E",
        },
        tertiary: {
          DEFAULT: "#BB8A52",
          foreground: "#BB8A52",
        },
        yellow: {
          DEFAULT: "#FFBA00",
          foreground: "#FFBA00",
        },
        brown: {
          DEFAULT: "#77542A",
          foreground: "#77542A",
        },
        destructive: {
          DEFAULT: "#F32C22",
          foreground: "#F32C22",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
      backgroundImage: {
        map: "url('/img/background.webp')",
      },
      boxShadow: {
        custom: "4px 4px 16px 0px rgba(0, 0, 0, 0.25)",
      },
      scale: {
        99: "99%",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
