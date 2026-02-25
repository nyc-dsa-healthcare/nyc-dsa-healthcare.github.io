"""
Pelican plugin: fetch upcoming events from Action Network at build time.

Requires env var ACTION_NETWORK_API_KEY. If unset, events will be empty
(safe for local dev without the key).
"""

import os
from datetime import datetime, timezone

import requests
from pelican import signals

BASE_URL = "https://actionnetwork.org/api/v2"


def _parse_dt(date_str):
    """Parse an Action Network ISO 8601 date string to an aware datetime."""
    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))


def _event_to_dict(raw):
    location = ""
    borough = ""
    if raw.get("location"):
        addr = raw["location"].get("address_lines") or []
        location = addr[0] if addr else "Virtual Event"
        borough = raw["location"].get("locality", "")

    links = raw.get("_links", {})
    signup_url = (
        links.get("osdi:record_attendance_helper", {}).get("href")
        or raw.get("browser_url", "")
    )

    date_str = raw.get("start_date", "")
    date_formatted = ""
    month_year = ""
    if date_str:
        dt = _parse_dt(date_str)
        # Convert to Eastern time for display (rough offset; DST not handled)
        date_formatted = dt.strftime("%-I:%M %p, %A %B %-d, %Y")
        month_year = dt.strftime("%Y-%m")  # used for groupby sort key
        month_label = dt.strftime("%B %Y")
    else:
        month_label = "Unknown"

    return {
        "id": raw["identifiers"][0] if raw.get("identifiers") else "",
        "name": raw.get("title", ""),
        "date": date_str,
        "date_formatted": date_formatted,
        "month_year": month_year,
        "month_label": month_label,
        "status": raw.get("status", ""),
        "description": raw.get("description", ""),
        "browser_url": raw.get("browser_url", ""),
        "signup_url": signup_url,
        "location": location,
        "borough": borough,
    }


def fetch_events(api_key):
    headers = {"OSDI-API-Token": api_key}
    events = []
    page = 1

    while True:
        resp = requests.get(
            f"{BASE_URL}/events",
            params={"page": page},
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        raw_events = data.get("_embedded", {}).get("osdi:events", [])
        total_pages = data.get("total_pages", 1)

        for raw in raw_events:
            events.append(_event_to_dict(raw))

        if page >= total_pages:
            break
        page += 1

    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    events = [
        e for e in events
        if e["status"] != "cancelled"
        and e["date"]
        and _parse_dt(e["date"]) >= today_start
    ]
    events.sort(key=lambda e: e["date"])
    return events


def add_events_to_context(pelican):
    api_key = os.environ.get("ACTION_NETWORK_API_KEY", "")
    if not api_key:
        print("action_network plugin: ACTION_NETWORK_API_KEY not set — events will be empty")
        pelican.settings["ACTION_NETWORK_EVENTS"] = []
        return

    try:
        events = fetch_events(api_key)
        pelican.settings["ACTION_NETWORK_EVENTS"] = events
        print(f"action_network plugin: fetched {len(events)} upcoming events")
    except Exception as exc:
        print(f"action_network plugin: ERROR fetching events — {exc}")
        pelican.settings["ACTION_NETWORK_EVENTS"] = []


def register():
    signals.initialized.connect(add_events_to_context)
