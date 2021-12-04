from enum import Enum
from time import sleep
from typing import Dict, List, Tuple

from scrapper.conf import BASE_URL
from scrapper.utilities.common import safely_click, safely_fill_input, split_name_amount, split_name_amount_with_date_ranges
from scrapper.types import BrowserType
from scrapper.utilities.presets import Inputs, Spans
from scrapper.utilities.url_param_extender import update_url
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def goto_front_page(driver: BrowserType):
	"""
	sets driver on BASE_URL webpage

	:param driver: driver to set
	:type driver: BrowserType
	"""
	if BASE_URL != driver.current_url:
		driver.get(BASE_URL)


def try_accept_cookies(driver: BrowserType):
	"""
	tries to accept banner on main site

	:param driver: driver on which cookie banner should be closed
	:type driver: BrowserType
	"""
	cookie_banner: List[WebElement] = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
	if len(cookie_banner) > 0:
		cookie_banner[0].click()


class FRONT_PAGE_TAB(Enum):
	"""
	describes tab on front page
	"""
	CARS = 0,
	PARTS = 1


def switch_category_tab(driver: BrowserType, tab: FRONT_PAGE_TAB):
	"""
	switches between available tabs

	:param driver: driver on which perform switching
	:type driver: BrowserType
	:param tab: tab to switch to
	:type tab: FRONT_PAGE_TAB
	"""
	if tab == FRONT_PAGE_TAB.CARS:
		driver.get(update_url(BASE_URL, category="osobowe"))
	elif tab == FRONT_PAGE_TAB.PARTS: # else is not used to prevent accident if more tabs will be handled
		driver.get(update_url(BASE_URL, category="czesci"))


def get_input_field_by_placeholder(driver: BrowserType, *, placeholder_text: str, switch_tab: FRONT_PAGE_TAB = None) -> WebElement:
	"""
	looks for input text field with given placeholder text on site, and returns

	:param driver: driver to use for lookup
	:type driver: BrowserType
	:param placeholder_text: this text should be in placeholder attribiute of found tag
	:type placeholder_text: str
	:param switch_tab: tab on which searchinbg should be performed, defaults to None
	:type switch_tab: FRONT_PAGE_TAB, optional
	:return: input text field
	:rtype: WebElement
	"""
	if switch_tab is not None:
		switch_category_tab(driver, switch_tab)
	result = Inputs(driver).attr_filter('placeholder', placeholder_text)
	assert len(result) > 0
	return list(result.values())[0]


def get_car_brands_input_field(driver: BrowserType, *, switch_tab: bool = True) -> WebElement:
	"""
	returns input field for setting brand of car

	:param driver: driver to use for lookup
	:type driver: BrowserType
	:param switch_tab: if set to true driver.get will be performed, defaults to True
	:type switch_tab: bool, optional
	:return: input text field
	:rtype: WebElement
	"""
	return get_input_field_by_placeholder(driver, placeholder_text='Marka', switch_tab=FRONT_PAGE_TAB.CARS if switch_tab else None)


def get_car_model_input_field(driver: BrowserType, *, switch_tab: bool = True) -> WebElement:
	"""
	returns input field for setting model of car

	:param driver: driver to use for lookup
	:type driver: BrowserType
	:param switch_tab: if set to true driver.get will be performed, defaults to True
	:type switch_tab: bool, optional
	:return: input text field
	:rtype: WebElement
	"""
	return get_input_field_by_placeholder(driver, placeholder_text='Model', switch_tab=FRONT_PAGE_TAB.CARS if switch_tab else None)


def get_car_generation_input_field(driver: BrowserType, *, switch_tab: bool = True) -> WebElement:
	"""
	returns input field for setting generation of car

	:param driver: driver to use for lookup
	:type driver: BrowserType
	:param switch_tab: if set to true driver.get will be performed, defaults to True
	:type switch_tab: bool, optional
	:return: input text field
	:rtype: WebElement
	"""
	return get_input_field_by_placeholder(driver, placeholder_text='Generacja', switch_tab=FRONT_PAGE_TAB.CARS if switch_tab else None)


def get_avaiable_car_brands(driver: BrowserType) -> Dict[str, int]:
	"""
	return dict of car brands with count of available records

	:param driver: driver to use for lookup
	:type driver: BrowserType
	:rtype: Dict[str, int]
	"""
	safely_click(get_car_brands_input_field(driver))
	car_brands = list(Spans(driver, By.XPATH, "//*[starts-with(@id, 'downshift-1-item-')]/div/span").content_dictionary().keys())
	return dict(sorted([split_name_amount(x) for x in car_brands], key=lambda x: x[1], reverse=True))


def get_avaiable_car_models(driver: BrowserType, brand: str) -> Dict[str, int]:
	"""
	return dict of car models for given brand with count of available records

	:param driver: driver to use for lookup
	:type driver: BrowserType
	:param brand: brand for which lookup of model is performed
	:type brand: str
	:rtype: Dict[str, int]
	"""
	safely_fill_input(get_car_brands_input_field(driver), brand)
	safely_click(get_car_model_input_field(driver, switch_tab=False))
	car_models = list(Spans(driver, By.XPATH, "//*[starts-with(@id, 'downshift-2-item-')]/div/span").content_dictionary().keys())
	return dict(sorted([split_name_amount(x) for x in car_models], key=lambda x: x[1], reverse=True))


def get_avaiable_car_generations(driver: BrowserType, brand: str, model: str) -> Dict[str, int]:
	"""
	return dict of car generations for given brand and model with count of available records

	:param driver: driver to use for lookup
	:type driver: BrowserType
	:param brand: brand for which lookup of generation is performed
	:type brand: str
	:param model: model for which lookup of generation is performed
	:type model: str
	:rtype: Dict[str, int]
	"""
	safely_fill_input(get_car_brands_input_field(driver), brand)
	safely_fill_input(get_car_model_input_field(driver, switch_tab=False), model)
	safely_click(get_car_generation_input_field(driver, switch_tab=False))
	car_models = list(Spans(driver, By.XPATH, "//*[starts-with(@id, 'downshift-3-item-')]/div/span").content_dictionary().keys())
	return dict(sorted([split_name_amount_with_date_ranges(x) for x in car_models], key=lambda x: x[1], reverse=True))
