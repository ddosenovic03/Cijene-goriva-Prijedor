from __future__ import annotations
import re
from bs4 import BeautifulSoup

FUEL_PATTERNS = {
    "Benzin 95" : r"Benzin 95\s+(\d+\.\d+)",
    "Dizel": r"Dizel\s+(\d+\.\d+)",
    "LPG": r"LPG\s+(\d+\.\d+)",
    "Super 98": r"Super 98\s+(\d+\.\d+)"
}

def parse_stations(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    stations = []

    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        if "/pumpa/" not in href:
            continue

        text = " ".join(link.stripped_strings)
        if not text:
            continue

        station_data = extract_station_data(text)
        if not station_data["fuels"]:
            continue

        station_data["url"] = (
            f"https://goriva.ba{href}" if href.startswith("/") else href
        )
        stations.append(station_data)

    # deduplikacija po nazivu + gorivima
    unique = {}
    for station in stations:
        key = (
            station["name"],
            tuple(sorted(station["fuels"].items()))
        )
        unique[key] = station

    return list(unique.values())


def extract_station_data(text: str) -> dict:
    text = " ".join(text.split())

    first_fuel_positions = []
    for fuel_name in FUEL_PATTERNS:
        match = re.search(re.escape(fuel_name), text)
        if match:
            first_fuel_positions.append(match.start())

    metadata_end = min(first_fuel_positions) if first_fuel_positions else len(text)
    metadata = text[:metadata_end].strip()

    fuels = {}
    for fuel_name, pattern in FUEL_PATTERNS.items():
        match = re.search(pattern, text)
        if match:
            fuels[fuel_name] = float(match.group(1))

    # malo čišćenje naziva
    metadata = re.sub(r"\s+", " ", metadata).strip()

    return {
        "name": metadata,
        "fuels": fuels,
    }