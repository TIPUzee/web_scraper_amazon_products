from __future__ import annotations

import copy
from typing import Dict, Optional, Union

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webdriver import WebElement

from model import ProductPathWithChildren, amazon_search_product, PropToSelect

driver: Chrome = None


def setup_driver(query: str) -> Chrome:
    global driver
    driver = webdriver.Chrome()
    driver.get(f'https://www.amazon.com/s?k={query}')

    for i in range(3):
        if 'Something went wrong!'.lower() in driver.title.lower():
            driver.refresh()
        else:
            break
    return driver


def set_css(element: WebElement) -> None:
    driver.execute_script("arguments[0].style.backgroundColor = '#ff00004e';", element)


# Refactored get_text function, receiving only parent_element, multiple, and children
def get_content(
    parent_element: WebElement,
    children: Optional[Dict[str, ProductPathWithChildren]] = None,
    toSelect: PropToSelect = 'text',
) -> any:
    try:
        if not parent_element:
            return None

        try:
            if children is None:
                set_css(parent_element)

                if toSelect == 'text':
                    return parent_element.text
                elif toSelect == 'href':
                    return parent_element.get_attribute('href')
                elif toSelect == 'src':
                    return parent_element.get_attribute('src')
                elif toSelect == 'textContent':
                    return parent_element.get_attribute('textContent')
                return None
        except:
            return None

        obj = {}
        for key, child in children.items():
            if child.get('multiple', False):
                child_elements = parent_element.find_elements(By.CSS_SELECTOR, child['path'])
                [set_css(element) for element in child_elements]

                obj[key] = [
                    get_content(
                        child_element,
                        child.get('children', None),
                        child.get('toSelect', 'text'),  # noqa
                    )
                    for child_element in child_elements
                ]
                continue

            child_element = parent_element.find_element(By.CSS_SELECTOR, child['path'])
            set_css(child_element)
            obj[key] = get_content(
                child_element,
                child.get('children', None),
                child.get('toSelect', 'text'),  # noqa
            )

        return obj

    except Exception as e:
        print(e)
        return None


# Function to fetch data using the product path
def fetch_data(query: str, path: ProductPathWithChildren) -> list[dict]:
    items = []
    driver = setup_driver(query)

    for page in range(2, 3):
        parent_element = driver.find_element(By.TAG_NAME, 'body')
        items += get_content(parent_element, {'products': path})['products']

        break
        driver.get(f'https://www.amazon.com/s?k={query}&page={page}')

    items = [item for item in items if item and item['title'] is not None and item['title'] != '']

    print('- ' * 10)

    import pprint
    pprint.pprint(items)
    return items


fetch_data('headphones', amazon_search_product)

# import time
#
# time.sleep(60)
