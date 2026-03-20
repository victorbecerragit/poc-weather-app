Created using AGENTS.md.

# weather-pavia

Real-time weather for Pavia, Italy, updated automatically with Open-Meteo.

## Key Features

- Fetches current weather (no API key required).
- Updates the README every 30 minutes via GitHub Actions.
- Optional Astro UI for a visual snapshot.

## Local Development

### Prerequisites

- Python 3.12

### Install Dependencies

```bash
pip install httpx
```

### Update README Locally

```bash
python fetch_weather.py
```

### Dry Run

```bash
python fetch_weather.py --dry-run
```

### Run Tests

```bash
python -m pytest tests/
```

## Current Weather

<!-- WEATHER:START -->
| Time (Europe/Rome) | Temp (°C) | Humidity (%) | Wind (km/h) | Wind Dir (°) | Precip (mm) | Code |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-03-20T09:45 | 9.2 | 64 | 4.1 | 195 | 0.0 | 1 🌤️ |
<!-- WEATHER:END -->

## Astro UI

Live UI: http://poc-weather-app.io

```bash
cd src
npm install
npm run dev
```
