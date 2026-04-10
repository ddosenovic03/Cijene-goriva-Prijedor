import requests

from app.config import BASE_URL, HEADERS

def fetch_html() -> str:
    """Fetches the HTML content of the target webpage."""
    try:
        response = requests.get(BASE_URL, headers=HEADERS, timeout=20)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return ""