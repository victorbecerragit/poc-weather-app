# AGENTS.md — weather-pavia

## Project purpose
This project fetches real-time weather for Pavia, Italy (lat 45.18, lon 9.15)
from the Open-Meteo API (no key needed) and injects a Markdown table into README.md.
A GitHub Actions cron job runs every 30 minutes and auto-commits the result.

## Architecture
- `fetch_weather.py` — Python script: calls Open-Meteo, rewrites the
  <!-- WEATHER:START --> / <!-- WEATHER:END --> block in README.md.
- `.github/workflows/update-weather.yml` — scheduler + git push.
- `src/` (optional) — Astro static site rendering the same data visually.

## Dev environment
- Python 3.12 required. Install deps: `pip install httpx`.
- To test locally: `python fetch_weather.py` then inspect README.md.
- For the Astro site: `npm install && npm run dev` from `src/`.
- Open-Meteo API URL: https://api.open-meteo.com/v1/forecast
  Params: latitude=45.18, longitude=9.15, timezone=Europe/Rome

## Weather variables available
- `temperature_2m` — air temperature at 2 m (°C)
- `relative_humidity_2m` — humidity (%)
- `wind_speed_10m` — wind speed at 10 m (km/h)
- `wind_direction_10m` — wind direction (°)
- `precipitation` — last-hour precipitation (mm)
- `weathercode` — WMO code (map to emoji in script)

## Testing instructions
- Run `python -m pytest tests/` to validate JSON parsing and regex replacement.
- Ensure the sentinel comments exist in README.md before running the script.
- Simulate a dry-run: `python fetch_weather.py --dry-run` (prints block, no write).

## CI/CD
- Workflow file: `.github/workflows/update-weather.yml`
- Trigger: cron every 30 min + manual `workflow_dispatch`.
- The bot commits only if README.md actually changed (`git diff --quiet`).
- Never push secrets; Open-Meteo requires no API key.

## PR instructions
- Title format: [weather-pavia] <Title>
- Run `python fetch_weather.py` locally and verify README output before opening a PR.
- Do not modify the sentinel HTML comments in README.md — they are required by the script.

## Extending the project
- Add more variables by appending to the `&current=` param in the API URL.
- For hourly forecasts, switch to `&hourly=temperature_2m,precipitation`.
- For the Astro layer, consume the same API in a `.astro` page using `fetch()` at build time or as a server endpoint.
