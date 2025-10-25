import os
from base64 import b64encode
import requests
from dotenv import load_dotenv, set_key, find_dotenv


# curl -X POST \
#   'https://api.kroger.com/v1/connect/oauth2/token' \
#   -H 'Content-Type: application/x-www-form-urlencoded' \
#   -H 'Authorization: Basic {{base64(CLIENT_ID:CLIENT_SECRET)}}' \
#   -d 'grant_type=client_credentials'

def get_token(client_id: str = None, client_secret: str = None) -> None:
    """
    Query and save a new Kroger API token to the local .env file.
    Each token is valid for 30 minutes.

    :param client_id: Client ID (leave blank to load key CLIENT_ID from .env)
    :param client_secret: Client Secret (leave blank to load key CLIENT_SECRET from .env)
    :return: None - modifies .env file
    """

    # Load .env variables
    load_dotenv()

    if client_id is None:
        client_id: str = os.getenv('CLIENT_ID')
    if client_secret is None:
        client_secret: str = os.getenv('CLIENT_SECRET')

    authkey: str = b64encode(bytes(f"{client_id}:{client_secret}", 'utf-8')).decode('utf-8')
    url = "https://api.kroger.com/v1/connect/oauth2/token"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {authkey}',
    }

    data = {
        'grant_type': 'client_credentials',
        'scope': 'product.compact'
    }


    response = requests.post(url, headers=headers, data=data)
    print(response.json())

    if response.status_code != 200:
        raise RuntimeError(response.json())

    token = response.json()['access_token']

    set_key(find_dotenv(), "TOKEN", token, quote_mode="never")

if __name__ == '__main__':
    get_token()