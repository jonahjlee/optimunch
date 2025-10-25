import pprint
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel, model_validator
from typing import Optional

load_dotenv()

class ProductQuery(BaseModel):
    term: Optional[str] = None
    productId: Optional[str] = None
    locationId: Optional[str] = None
    brand: Optional[str] = None
    fulfillment: Optional[str] = None
    start: Optional[str] = None
    limit: Optional[str] = None

    # Useful errors are already returned for invalid inputs...
    # @model_validator(mode="after")
    # def _has_term_or_productid(self):
    #     """Ensure the document has one of 'term' or 'product_id' set."""
    #     if not (self.term is not None
    #             or self.product_id is not None):
    #         raise ValueError("Field 'term' or 'product_id' must be used to request product information.")
    #     return self


def query_product(query: ProductQuery, token: str = None) -> dict:
    if token is None:
        token = os.environ.get("TOKEN")

    url: str = "https://api.kroger.com/v1/products?"
    for key, value in query.model_dump(exclude_none=True).items():
        print(value)
        value_formatted = value.replace(" ", "%20")
        url += f"filter.{key}={value_formatted}&"
    url = url[:-1]

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
            'error': f"Failed to fetch products. Status code: {response.status_code}",
            'message': response.text
        }

if __name__ == "__main__":

    query = ProductQuery(term='carrot')
    products = query_product(query)

    # Print the results
    pprint.pp(products)
