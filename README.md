Created using AGENTS.md.


# weather-pavia

Real-time weather for Pavia, Italy, updated automatically with Open-Meteo.

## Key Features

- Fetches current weather (no API key required).
- Updates the README every 15 minutes via GitHub Actions.
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
    <div style="font-size:28px;font-weight:700;margin:6px 0;">☁️ 15.3&deg;C</div>
    <div style="font-size:12px;color:#9c98ad;">Updated 2026-03-28T19:00</div>
    <div style="margin-top:8px;font-size:12px;color:#d6d0ff;">Humidity 41% · Wind 4.3 km/h</div>
  </div>
</div>

| Time (Europe/Rome) | Temp (°C) | Humidity (%) | Wind (km/h) | Wind Dir (°) | Precip (mm) | Code |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-03-28T19:00 | 15.3 | 41 | 4.3 | 222 | 0.0 | 3 ☁️ |
<!-- WEATHER:END -->

## Astro UI

Live UI: <https://poc-weather-app.victorbecerragit.dev>

### Query the API (weather.json)

You can fetch the current weather data directly from the Astro API route:

- **Local development:**

  ```bash
  curl -i http://localhost:4322/api/weather.json
  ```

- **From the deployed site:**

  ```bash
  curl -i https://poc-weather-app.victorbecerragit.dev/api/weather.json
  ```

---

```bash
cd src
npm install
npm run dev
```
