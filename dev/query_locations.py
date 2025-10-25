import pprint
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel, model_validator
from typing import Optional

load_dotenv()


def query_location_from_zip_code(zip_code: str, token: str = None) -> dict:
    if token is None:
        token = os.environ.get("TOKEN")

    url: str = f"https://api.kroger.com/v1/locations&filter.zipCode.near={zip_code}"

    headers: dict = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response: requests.Response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            'error': f"Failed to fetch locations. Status code: {response.status_code}",
            'message': response.text
        }


def query_location_from_lat_lon(lat: str | float,
                                lon: str | float,
                                limit: int = 10,
                                token: str = None) -> dict:
    if token is None:
        token = os.environ.get("TOKEN")

    url: str = (f"https://api.kroger.com/v1/locations"
                f"&filter.lat.near={lat}"
                f"&filter.lon.near={lon}"
                f"&filter.limit={limit}")
    print(url)
    headers: dict = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response: requests.Response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            'error': f"Failed to fetch locations. Status code: {response.status_code}",
            'message': response.text
        }


if __name__ == "__main__":
    # locations = query_location_from_zip_code('V7L 2V2')
    locations = query_location_from_lat_lon(-50, -50)

    # Print the results
    pprint.pp(locations)
