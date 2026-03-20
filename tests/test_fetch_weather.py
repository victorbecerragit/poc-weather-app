"""Tests for fetch_weather module."""

from __future__ import annotations

import pytest

from fetch_weather import (
    WEATHER_END,
    WEATHER_START,
    WeatherData,
    build_api_url,
    build_weather_block,
    parse_current_weather,
    render_markdown_table,
    replace_weather_block,
    weathercode_to_emoji,
)


def test_build_api_url_includes_params() -> None:
    url = build_api_url()
    assert "latitude=45.18" in url
    assert "longitude=9.15" in url
    assert "timezone=Europe%2FRome" in url
    assert "current=temperature_2m%2Crelative_humidity_2m" in url


def test_parse_current_weather_valid() -> None:
    payload = {
        "current": {
            "time": "2026-03-20T12:00",
            "temperature_2m": 12.5,
            "relative_humidity_2m": 55,
            "wind_speed_10m": 9.1,
            "wind_direction_10m": 180,
            "precipitation": 0.0,
            "weathercode": 2,
        }
    }
    data = parse_current_weather(payload)
    assert data.temperature_c == 12.5
    assert data.humidity_percent == 55
    assert data.wind_speed_kmh == 9.1
    assert data.wind_direction_deg == 180
    assert data.precipitation_mm == 0.0
    assert data.weathercode == 2


def test_weathercode_to_emoji_default() -> None:
    assert weathercode_to_emoji(999) == "\u2754"


def test_render_markdown_table() -> None:
    data = WeatherData(
        time="2026-03-20T12:00",
        temperature_c=12.5,
        humidity_percent=55,
        wind_speed_kmh=9.1,
        wind_direction_deg=180,
        precipitation_mm=0.0,
        weathercode=2,
    )
    table = render_markdown_table(data)
    assert "| Time (Europe/Rome)" in table
    assert "| 2026-03-20T12:00" in table
    assert "| 12.5" in table


def test_build_weather_block() -> None:
    block = build_weather_block("| table |")
    assert block.startswith(WEATHER_START)
    assert block.endswith(WEATHER_END)


def test_replace_weather_block_success() -> None:
    content = (
        "# Title\n\n"
        f"{WEATHER_START}\nold\n{WEATHER_END}\n"
        "\nFooter"
    )
    block = build_weather_block("new")
    updated = replace_weather_block(content, block)
    assert "new" in updated
    assert "old" not in updated


def test_replace_weather_block_missing_raises() -> None:
    with pytest.raises(ValueError):
        replace_weather_block("no markers", "block")
