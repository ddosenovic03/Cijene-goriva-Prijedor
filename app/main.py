from app.fetch import fetch_html
from app.parser import parse_stations
from app.services import calculate_fuel_statistics


def print_report(stats: dict) -> None:
    print("=" * 50)
    print("CIJENE GORIVA - PRIJEDOR")
    print("=" * 50)

    for fuel_name, data in stats.items():
        print(f"\n{fuel_name}")
        print(f"  Prosječna cijena: {data['average_price']:.3f} KM/l")
        print(f"  Broj pumpi: {data['stations_count']}")
        print(f"  Najjeftinije: {data['cheapest']['station']}")
        print(f"  Cijena: {data['cheapest']['price']:.3f} KM/l")
        print(f"  Link: {data['cheapest']['url']}")


def main() -> None:
    try:
        html = fetch_html()
        stations = parse_stations(html)

        print("\nDEBUG - PARSIRANE STANICE")
        for station in stations:
            print(station)

        if not stations:
            print("Nema pronađenih pumpi za Prijedor.")
            return

        stats = calculate_fuel_statistics(stations)
        print_report(stats)

    except Exception as exc:
        print(f"Došlo je do greške: {exc}")


if __name__ == "__main__":
    main()