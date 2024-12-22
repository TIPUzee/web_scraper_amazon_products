from __future__ import annotations

from typing import Dict, TypedDict, Optional
from typing import Literal

PropToSelect = Literal['text', 'href', 'src', 'textContent']


# Define the recursive type for the ProductDict
class ProductPathWithoutChildren(TypedDict):
    path: str
    multiple: Optional[bool]
    toSelect: PropToSelect


# Define the recursive type for the ProductDict
class ProductPathWithChildren(TypedDict):
    path: str
    multiple: Optional[bool]
    children: Optional[Dict[str, 'ProductPathWithChildren' | 'ProductPathWithChildren']]


amazon_search_product: ProductPathWithChildren = {
    'path':     '.puisg-row:has( .puisg-row)',
    'children': {
        'title':     {'path': '[data-cy="title-recipe"] a.a-link-normal'},
        'image_url': {'path': '[data-cy="image-container"] img', 'toSelect': 'src'},
        'reviews':   {'path': '[data-cy="reviews-ratings-slot"] span', 'toSelect': 'textContent'},
        'price':     {
            'path': ':is([data-cy="price-recipe"] .a-offscreen,'
                    '[data-cy="secondary-offer-recipe]>div>div:nth-child(2))',
        },
    },
    'multiple': True,
}
