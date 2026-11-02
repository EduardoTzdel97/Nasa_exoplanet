import requests


API_URL = " https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

QUERY = """
SELECT pl_name, pl_orbper, pl_rade, pl_bmasse, st_teff, st_rad, st_mass
FROM pscomppars
ORDER BY pl_name

"""


def fetch_sample():
    """
    Fetches a sample of exoplanet data from the NASA Exoplanet Archive.

    Returns:
        list: A list of dictionaries containing exoplanet data.
    """
    response = requests.post(API_URL, data={"query": QUERY, "format": "json"},
                             timeout=10)  # Set a timeout for the request
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()


def main() -> None:
    """
    Main function to fetch and print the exoplanet data sample.
    """
    try:
        sample_data = fetch_sample()
        for planet in sample_data:
            print(planet)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")

if __name__ == "__main__":
    main()