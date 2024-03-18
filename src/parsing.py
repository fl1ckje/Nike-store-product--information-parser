import json
from pathlib import Path
from time import sleep
from typing import Union
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

from src.config import DOWNLOADS_PATH, HEADLESS, GECKO_DRIVER_PATH, NIKE_DATA_PATH, SAVE_PRODUCT_TO_FILE, SCROLL_PAUSE_TIME
from src.nike_product_page.xpath import *
from src.nike_product_list.xpath import *


def init_geckodriver() -> WebDriver:
    gecko_driver_path = GECKO_DRIVER_PATH
    service = Service(executable_path=gecko_driver_path)
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")

    return Firefox(options=options, service=service)


def accept_cookie(driver: WebDriver):
    # try to accept cookies if needed
    try:
        cookie_btn = driver.find_element(By.XPATH, COOKIE_BTN_XPATH)
        cookie_btn.click()
        print("==> Cookie accept successful")

    except WebDriverException:
        print("==> Cookie accept failed")


def parse_nike_product_page(url: str):
    """
    Parses product page from https://www.nike.com/th/
    """
    driver = init_geckodriver()

    try:
        # get target page
        driver.get(url)

        accept_cookie(driver)

        product = {}

        # title
        product["title"] = driver.find_element(
            By.XPATH, TITLE_XPATH).get_attribute("innerHTML")

        # subtitle
        product["subtitle"] = driver.find_element(
            By.XPATH, SUBTITLE_XPATH).get_attribute("innerHTML")

        # vendor
        product["vendor"] = product["title"].split()[0]

        # color
        color = driver.find_element(
            By.XPATH, COLOR_XPATH).get_attribute("innerHTML")
        product["color"] = color[color.find(":") + 2:]

        # style
        size = driver.find_element(
            By.XPATH, STYLE_XPATH).get_attribute("innerHTML")
        product["style"] = size[size.find(":") + 2:]

        # description
        product["description"] = driver.find_element(
            By.XPATH, DESCRIPTION_XPATH).get_attribute("innerHTML")

        # price
        product["price"] = driver.find_element(By.XPATH, PRICE_XPATH).get_attribute(
            "innerHTML").replace(",", "").replace("฿", "")

        # available sizes
        sizes = []
        for sizes_cell in driver.find_element(By.XPATH, SIZES_GRID_XPATH).find_elements(By.TAG_NAME, "div"):
            if sizes_cell.find_element(By.TAG_NAME, "input").get_attribute("disabled") is None:
                sizes.append(sizes_cell.find_element(
                    By.TAG_NAME, "label").get_attribute("innerHTML"))
        product["sizes"] = sizes

        # images
        img_container = driver.find_element(By.XPATH, IMG_CONTAINER_XPATH)
        imgs = img_container.find_elements(By.TAG_NAME, "img")
        images = []
        for img in imgs:
            images.append(img.get_attribute("src"))
        product["images"] = images
        driver.quit()

        if SAVE_PRODUCT_TO_FILE:
            SAVE_PATH = DOWNLOADS_PATH / f"{product['title']}.json"
            with open(SAVE_PATH, "w") as file:
                json.dump(product, file)
                print(f'==> Saved product: {SAVE_PATH}')
        return product
    except Exception as e:
        driver.quit()
        return None   


def parse_nike_product_list(txt_path: Union[str, Path]) -> dict:
    """
    Parses product list from https://www.nike.com/th/
    """
    driver = init_geckodriver()

    try:
        driver.get("https://www.nike.com/th/")
        accept_cookie(driver)

        nike_cats = []
        with open(txt_path, "r") as file:
            nike_cats = file.readlines()

        idx = 0
        products_links_dict = {}
        for i in nike_cats:
            print(f"[{i}]:\nlink: {i}\n")
            products_links = get_category_products_links(driver, i)
            SAVE_PATH = DOWNLOADS_PATH / f"nike_data_{idx}.json"
            with open(SAVE_PATH, "w") as file:
                json.dump(products_links, file)
                print(f'==> Saved product list: {SAVE_PATH}')
            products_links_dict[idx] = products_links
            idx += 1
        driver.quit()

        return products_links_dict
    except Exception as e:
        driver.quit()
        return None


def get_category_products_links(driver: WebDriver, url: str) -> list:
    def get_doc_scroll_height():
        return int(driver.execute_script("return document.documentElement.scrollHeight"))

    def all_elements_equal(list: list):
        return all(i == list[0] for i in list)

    print('==> Loading category page...')
    driver.get(url)
    # sleep(4)
    print('==> Scrolling...')

    new_scroll_height = 0
    prev_doc_scroll_height = 0
    current_doc_scroll_height = 0
    scroll_heights = []
    scroll_count = 0
    i = 0

    while True:
        new_scroll_height += 150
        driver.execute_script(f"window.scrollTo(0, {new_scroll_height});")
        current_doc_scroll_height = get_doc_scroll_height()
        scroll_heights.append(current_doc_scroll_height)
        scroll_count += 1

        if current_doc_scroll_height != prev_doc_scroll_height:
            prev_doc_scroll_height = current_doc_scroll_height
            scroll_count = 0
            scroll_heights.clear()

        if len(scroll_heights) > 50:
            if all_elements_equal(scroll_heights):
                print("==> Reached the end of page. Collecting products links...")
                break
            else:
                scroll_heights.clear()

        sleep(SCROLL_PAUSE_TIME)

    products_links = []
    i = 1

    for product_card in driver.find_elements(By.XPATH, f"//a[contains(@class, '{PRODUCT_CARD_LINK_CSS}')]"):
        link = product_card.get_attribute('href')
        products_links.append(link)
        i += 1

    return products_links
