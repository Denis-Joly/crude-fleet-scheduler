import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  // Relative asset paths so Streamlit can serve the bundled component from
  // its component-scoped URL. Without this, built index.html references
  // /assets/... which 404s on Streamlit Cloud.
  base: "./",
  plugins: [react()],
  server: {
    port: 3001,
    strictPort: true,
  },
  build: {
    outDir: "build",
    emptyOutDir: true,
  },
});
