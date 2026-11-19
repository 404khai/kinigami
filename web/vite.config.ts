import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// A single-page app: /blog and /blog/:slug are client routes (see src/main.tsx).
// Hosts must rewrite unknown paths to /index.html; vercel.json does that.
export default defineConfig({
  plugins: [react()],
});
