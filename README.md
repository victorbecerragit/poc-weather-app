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
<div align="center">
  <div style="display:inline-block;padding:14px 18px;border-radius:16px;border:1px solid #2df2ff;background:#0f1118;color:#f7f4ff;font-family:Arial,sans-serif;">
    <div style="font-size:12px;letter-spacing:0.18em;text-transform:uppercase;color:#9c98ad;">Pavia Weather</div>
    <div style="font-size:28px;font-weight:700;margin:6px 0;">☁️ 6.7&deg;C</div>
    <div style="font-size:12px;color:#9c98ad;">Updated 2026-03-22T07:45</div>
    <div style="margin-top:8px;font-size:12px;color:#d6d0ff;">Humidity 69% · Wind 9.5 km/h</div>
  </div>
</div>

| Time (Europe/Rome) | Temp (°C) | Humidity (%) | Wind (km/h) | Wind Dir (°) | Precip (mm) | Code |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-03-22T07:45 | 6.7 | 69 | 9.5 | 61 | 0.0 | 3 ☁️ |
<!-- WEATHER:END -->

## Astro UI

Live UI: <https://poc-weather-app.victorbecerragit.dev> 

```bash
cd src
npm install
npm run dev
```
