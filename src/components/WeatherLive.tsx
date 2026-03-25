import { useEffect, useState } from 'react';

export type CurrentWeather = {
  time: string;
  temperature_2m: number;
  relative_humidity_2m: number;
  wind_speed_10m: number;
  wind_direction_10m: number;
  precipitation: number;
  weathercode: number;
};

const defaultWeather: CurrentWeather = {
  time: "--",
  temperature_2m: 0,
  relative_humidity_2m: 0,
  wind_speed_10m: 0,
  wind_direction_10m: 0,
  precipitation: 0,
  weathercode: 0
};

const emojiMap: Record<number, string> = {
  0: "\u2600\uFE0F",
  1: "\u{1F324}\uFE0F",
  2: "\u26C5",
  3: "\u2601\uFE0F",
  45: "\u{1F32B}\uFE0F",
  48: "\u{1F32B}\uFE0F",
  51: "\u{1F326}\uFE0F",
  53: "\u{1F326}\uFE0F",
  55: "\u{1F326}\uFE0F",
  61: "\u{1F327}\uFE0F",
  63: "\u{1F327}\uFE0F",
  65: "\u{1F327}\uFE0F",
  71: "\u{1F328}\uFE0F",
  73: "\u{1F328}\uFE0F",
  75: "\u{1F328}\uFE0F",
  80: "\u{1F327}\uFE0F",
  81: "\u{1F327}\uFE0F",
  82: "\u{1F327}\uFE0F",
  85: "\u{1F328}\uFE0F",
  86: "\u{1F328}\uFE0F",
  95: "\u26C8\uFE0F",
  96: "\u26C8\uFE0F",
  99: "\u26C8\uFE0F"
};

function getEmoji(code: number): string {
  return emojiMap[code] ?? "\u2754";
}

export default function WeatherLive() {
  const [weather, setWeather] = useState<CurrentWeather>(defaultWeather);
  const [status, setStatus] = useState('Loading...');

  useEffect(() => {
    // Fetch weather.json with a cache-busting query param to force the browser to bypass cache.
    // This ensures the frontend always gets the latest data, even if the browser would normally cache the static file.
    async function fetchWeather() {
      try {
        // Fetch from the Astro API route, not the static file
        const res = await fetch(`/api/weather.json?t=${Date.now()}`);
        if (!res.ok) throw new Error('No weather data');
        const data = await res.json();
        setWeather(data);
        setStatus('Live');
      } catch {
        setStatus('Offline');
      }
    }
    fetchWeather();
    // Refresh every 1 minute (60000 ms) for local testing
    const interval = setInterval(fetchWeather, 60000);
    return () => clearInterval(interval);
  }, []);


  // Map weather codes to dynamic titles
  function getDynamicTitle(code: number): string {
    if ([0, 1].includes(code)) return "Sunny Skies over Pavia";
    if ([2, 3].includes(code)) return "Cloudy Skies over Pavia";
    if ([45, 48].includes(code)) return "Foggy Morning in Pavia";
    if ([51, 53, 55, 61, 63, 65, 80, 81, 82].includes(code)) return "Rainy Day in Pavia";
    if ([71, 73, 75, 85, 86].includes(code)) return "Snowy Day in Pavia";
    if ([95, 96, 99].includes(code)) return "Stormy Weather in Pavia";
    return "Skies over Pavia";
  }

  const emoji = getEmoji(weather.weathercode);
  const dynamicTitle = getDynamicTitle(weather.weathercode);

  return (
    <div>
      <div className="hero__badge">
        <span>Weather Pavia Live</span>
        <span className="hero__status">{status}</span>
      </div>
      <h1>{dynamicTitle}</h1>
      <div className="hero__summary">
        <div className="temp">
          <div className="temp__emoji">{emoji}</div>
          <div className="temp__value">{weather.temperature_2m.toFixed(1)}</div>
          <div className="temp__unit">°C</div>
          <div className="temp__time">Updated {weather.time}</div>
        </div>
        <p>
          Real-time conditions for Pavia, Italy. Updated directly from Open-Meteo and
          reflected in the repository README.
        </p>
      </div>
      <section className="grid">
        <article className="card">
          <div className="card__title">Humidity</div>
          <div className="card__value humidity">{weather.relative_humidity_2m}%</div>
          <div className="card__meta">Relative humidity</div>
        </article>
        <article className="card">
          <div className="card__title">Wind</div>
          <div className="card__value wind">{weather.wind_speed_10m} km/h</div>
          <div className="card__meta wind">Direction {weather.wind_direction_10m}°</div>
        </article>
        <article className="card">
          <div className="card__title">Precipitation</div>
          <div className="card__value precip">{weather.precipitation} mm</div>
          <div className="card__meta">Last hour</div>
        </article>
      </section>
      <section className="footer">
        <div>
          <strong>Coordinates</strong>
          <span>45.18, 9.15</span>
        </div>
        <div>
          <strong>Timezone</strong>
          <span>Europe/Rome</span>
        </div>
        <div>
          <strong>API</strong>
          <span>Open-Meteo</span>
        </div>
      </section>
    </div>
  );
}
