from __future__ import annotations
from statistics import mean

def calculate_fuel_statistics(stations: list[dict]) -> dict:
    fuel_names = sorted({fuel for s in stations for fuel in s["fuels"].keys()})
    results = {}

    for fuel_name in fuel_names:
        offers = []

        for station in stations:
            if fuel_name in station["fuels"]:
                offers.append(
                    {
                        "station": station["name"],
                        "price": station["fuels"][fuel_name],
                        "url": station["url"],
                    }
                )

        # print(f"\nDEBUG - {fuel_name}")
        # for offer in offers:
        #     print(offer)

        if not offers:
            continue

        avg_price = mean(o["price"] for o in offers)
        cheapest = min(offers, key=lambda item: item["price"])

        results[fuel_name] = {
            "average_price": avg_price,
            "stations_count": len(offers),
            "cheapest": cheapest,
        }

    return results