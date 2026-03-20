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
| 2026-03-20T10:00 | 9.5 | 63 | 4.1 | 195 | 0.0 | 0 ☀️ |
<!-- WEATHER:END -->

## Astro UI

```bash
cd src
npm install
npm run dev
```
