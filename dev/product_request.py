import pprint
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def query_product(token: str = None, **kwargs):
    if token is None:
        token = os.environ.get("TOKEN")

    url = "https://api.kroger.com/v1/products?"
    for key, value in kwargs.items():
        value_formatted = value.replace(" ", "%20")
        url += f"{key}={value_formatted}&"
    url = url[:-1]

    print(url)

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            'error': f"Failed to fetch products. Status code: {response.status_code}",
            'message': response.text
        }

if __name__ == "__main__":

    args = {
        'filter.term': 'chicken soup',
    }

    products = query_product(**args)

    # Print the results
    pprint.pp(products)
