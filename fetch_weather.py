"""Fetch current weather and update README.md with a markdown table."""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlencode

import httpx

API_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = 45.18
LONGITUDE = 9.15
TIMEZONE = "Europe/Rome"

WEATHER_START = "<!-- WEATHER:START -->"
WEATHER_END = "<!-- WEATHER:END -->"

CURRENT_FIELDS = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "wind_direction_10m",
    "precipitation",
    "weathercode",
]

WEATHERCODE_EMOJI = {
    0: "\u2600\ufe0f",
    1: "\U0001F324\ufe0f",
    2: "\u26c5",
    3: "\u2601\ufe0f",
    45: "\U0001F32B\ufe0f",
    48: "\U0001F32B\ufe0f",
    51: "\U0001F326\ufe0f",
    53: "\U0001F326\ufe0f",
    55: "\U0001F326\ufe0f",
    56: "\U0001F327\ufe0f",
    57: "\U0001F327\ufe0f",
    61: "\U0001F327\ufe0f",
    63: "\U0001F327\ufe0f",
    65: "\U0001F327\ufe0f",
    66: "\U0001F327\ufe0f",
    67: "\U0001F327\ufe0f",
    71: "\U0001F328\ufe0f",
    73: "\U0001F328\ufe0f",
    75: "\U0001F328\ufe0f",
    77: "\U0001F328\ufe0f",
    80: "\U0001F327\ufe0f",
    81: "\U0001F327\ufe0f",
    82: "\U0001F327\ufe0f",
    85: "\U0001F328\ufe0f",
    86: "\U0001F328\ufe0f",
    95: "\u26c8\ufe0f",
    96: "\u26c8\ufe0f",
    99: "\u26c8\ufe0f",
}


@dataclass(frozen=True)
class WeatherData:
    """Current weather data returned by the Open-Meteo API.

    Attributes:
        time: ISO timestamp for the current observation.
        temperature_c: Air temperature in Celsius.
        humidity_percent: Relative humidity percentage.
        wind_speed_kmh: Wind speed in km/h.
        wind_direction_deg: Wind direction in degrees.
        precipitation_mm: Last hour precipitation in mm.
        weathercode: WMO weather code.
    """

    time: str
    temperature_c: float
    humidity_percent: float
    wind_speed_kmh: float
    wind_direction_deg: float
    precipitation_mm: float
    weathercode: int


def build_api_url() -> str:
    """Build the Open-Meteo API URL for current weather data.

    Returns:
        Fully encoded API URL string.
    """

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "timezone": TIMEZONE,
        "current": ",".join(CURRENT_FIELDS),
    }
    return f"{API_URL}?{urlencode(params)}"


def _require_key(mapping: Mapping[str, Any], key: str) -> Any:
    """Return a required key from a mapping or raise a ValueError.

    Args:
        mapping: Mapping to read from.
        key: Key to retrieve.

    Returns:
        The value from the mapping.

    Raises:
        ValueError: If the key is missing.
    """

    if key not in mapping:
        raise ValueError(f"Missing key '{key}' in API response")
    return mapping[key]


def parse_current_weather(payload: Mapping[str, Any]) -> WeatherData:
    """Parse the Open-Meteo response payload into WeatherData.

    Args:
        payload: Decoded JSON payload.

    Returns:
        Parsed WeatherData instance.

    Raises:
        ValueError: If required fields are missing.
    """

    current = _require_key(payload, "current")
    if not isinstance(current, Mapping):
        raise ValueError("'current' must be an object")

    return WeatherData(
        time=str(_require_key(current, "time")),
        temperature_c=float(_require_key(current, "temperature_2m")),
        humidity_percent=float(_require_key(current, "relative_humidity_2m")),
        wind_speed_kmh=float(_require_key(current, "wind_speed_10m")),
        wind_direction_deg=float(_require_key(current, "wind_direction_10m")),
        precipitation_mm=float(_require_key(current, "precipitation")),
        weathercode=int(_require_key(current, "weathercode")),
    )


def weathercode_to_emoji(code: int) -> str:
    """Map WMO weather codes to a display emoji.

    Args:
        code: WMO weather code.

    Returns:
        Emoji string.
    """

    return WEATHERCODE_EMOJI.get(code, "\u2754")


def render_markdown_table(data: WeatherData) -> str:
    """Render a markdown table for the current weather.

    Args:
        data: Weather data to render.

    Returns:
        Markdown table as a string.
    """

    emoji = weathercode_to_emoji(data.weathercode)
    return (
        "| Time (Europe/Rome) | Temp (\u00b0C) | Humidity (%) | Wind (km/h) | Wind Dir (\u00b0) | Precip (mm) | Code |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
        f"| {data.time} | {data.temperature_c:.1f} | {data.humidity_percent:.0f} | "
        f"{data.wind_speed_kmh:.1f} | {data.wind_direction_deg:.0f} | {data.precipitation_mm:.1f} | "
        f"{data.weathercode} {emoji} |"
    )


def build_weather_block(table: str) -> str:
    """Wrap a markdown table in the README weather sentinel comments.

    Args:
        table: Markdown table string.

    Returns:
        Weather block string.
    """

    return f"{WEATHER_START}\n{table}\n{WEATHER_END}"


def replace_weather_block(content: str, block: str) -> str:
    """Replace the weather block in README content.

    Args:
        content: Existing README content.
        block: New weather block.

    Returns:
        Updated README content.

    Raises:
        ValueError: If the weather block markers are missing.
    """

    pattern = re.compile(
        rf"{re.escape(WEATHER_START)}.*?{re.escape(WEATHER_END)}",
        re.DOTALL,
    )
    if not pattern.search(content):
        raise ValueError("README is missing WEATHER markers")
    return pattern.sub(block, content, count=1)


def update_readme(readme_path: Path, block: str) -> bool:
    """Update README.md with the provided weather block.

    Args:
        readme_path: Path to README.md.
        block: Weather block content.

    Returns:
        True if the file changed; otherwise False.
    """

    content = readme_path.read_text(encoding="utf-8")
    updated = replace_weather_block(content, block)
    if updated == content:
        return False
    readme_path.write_text(updated, encoding="utf-8")
    return True


async def fetch_current_weather() -> WeatherData:
    """Fetch current weather data from Open-Meteo.

    Returns:
        Parsed WeatherData.
    """

    url = build_api_url()
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        payload = response.json()
    return parse_current_weather(payload)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed argparse namespace.
    """

    parser = argparse.ArgumentParser(description="Update README.md with Pavia weather.")
    parser.add_argument(
        "--readme",
        default="README.md",
        help="Path to README.md",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the weather block without writing",
    )
    return parser.parse_args()


def run() -> int:
    """Run the weather update process.

    Returns:
        Process exit code.
    """

    args = parse_args()
    readme_path = Path(args.readme)

    if not readme_path.exists():
        print(f"README not found at {readme_path}", file=sys.stderr)
        return 1

    try:
        data = asyncio.run(fetch_current_weather())
        table = render_markdown_table(data)
        block = build_weather_block(table)
        if args.dry_run:
            print(block)
            return 0

        changed = update_readme(readme_path, block)
        if changed:
            print("README.md updated.")
        else:
            print("README.md already up to date.")
        return 0
    except (httpx.HTTPError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
