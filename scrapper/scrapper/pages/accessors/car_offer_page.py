from typing import Dict, List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from scrapper.pages.accessors.car_list import is_car_offer_link
from scrapper.utilities.common import element_dictionary
from scrapper.types import BrowserType


def validate_offer_link(link: str):
	assert is_car_offer_link(link)


def extract_detail_label(element: WebElement) -> str:
	return element.find_element(By.CLASS_NAME, 'offer-params__label').text


def extract_detail_value(element: WebElement) -> str:
	div: WebElement = element.find_element(By.CLASS_NAME, 'offer-params__value')
	a_hrefs: List[WebElement] = div.find_elements(By.TAG_NAME, 'a')
	return a_hrefs[0].text if len(a_hrefs) > 0 else div.text


def extract_image_link(x: WebElement) -> str:
	return x.find_element(By.TAG_NAME, 'img').get_attribute('src')


def remove_resolution_from_image_link(x: WebElement) -> str:
	link = extract_image_link(x)
	return link.split(';')[0]


def get_offer_details(driver: BrowserType, offer_link: str) -> Dict[str, str]:
	validate_offer_link(offer_link)
	driver.get(offer_link)
	elements = element_dictionary(driver, By.CLASS_NAME, "offer-params__item", extract_detail_label)
	return {key: extract_detail_value(value) for key, value in elements.items()}


def get_offer_images(driver: BrowserType, offer_link: str) -> List[str]:
	validate_offer_link(offer_link)
	driver.get(offer_link)
	return [remove_resolution_from_image_link(x) for x in driver.find_elements(By.CLASS_NAME, 'offer-photos-thumbs__item')]
