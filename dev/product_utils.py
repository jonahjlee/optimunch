from query_products import ProductQuery, query_product

def clip_description(description: str, cutoff: int = 50) -> str:
    if len(description) <= cutoff:
        return description
    return description[:cutoff - 3] + "..."

def print_product_names(term: str, locationId: str = None, limit: int = 50):
    query = ProductQuery(term=term, locationId=locationId, limit=limit)
    response = query_product(query)
    for product in response['data']:
        print(product['description'])

def print_product_prices(term: str, locationId: str , limit: int = 50):
    query = ProductQuery(term=term, locationId=locationId, limit=limit)
    response = query_product(query)

    descriptions = []
    prices = []
    for product in response['data']:
        try:
            descriptions.append(clip_description(product['description']))
            prices.append(product['items'][0]['price']['regular'])
        except KeyError:
            pass

    description_max_len = max(len(description) for description in descriptions)
    formatter = '{:<' + str(description_max_len) + '}'
    for description, price in zip(descriptions, prices):
        print(formatter.format(description), f'${price:0.2f}')


if __name__ == "__main__":
    print_product_prices('carrot', '01400413')