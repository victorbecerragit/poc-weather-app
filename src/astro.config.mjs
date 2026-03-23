

import { defineConfig } from "astro/config";
import react from "@astrojs/react";

export default defineConfig({
  site: "https://poc-weather-app.victorbecerragit.dev",
  base: "/",
  integrations: [react()],
  vite: {
    plugins: [],
  },
});
