


import { defineConfig } from "astro/config";
import react from "@astrojs/react";

// Vite plugin to watch weather.json and trigger HMR reload
import path from 'path';
import { fileURLToPath } from 'url';

function WeatherJsonHMR() {
  return {
    name: 'watch-weather-json',
    configureServer(server) {
      const __filename = fileURLToPath(import.meta.url);
      const __dirname = path.dirname(__filename);
      const file = path.resolve(__dirname, 'public/weather.json');
      server.watcher.add(file);
      server.watcher.on('change', (changed) => {
        if (changed === file) {
          server.ws.send({ type: 'full-reload', path: '*' });
        }
      });
    },
  };
}

export default defineConfig({
  root: "src/",
  site: "https://poc-weather-app.victorbecerragit.dev",
  base: "/",
  integrations: [react()],
  vite: {
    plugins: [WeatherJsonHMR()],
  },
});
