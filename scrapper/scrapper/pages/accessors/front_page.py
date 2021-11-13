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
	driver.get(BASE_URL)


def try_accept_cookies(driver: BrowserType):
	cookie_banner: List[WebElement] = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
	if len(cookie_banner) > 0:
		cookie_banner[0].click()


class FRONT_PAGE_TAB(Enum):
	CARS = 0,
	PARTS = 1


def switch_category_tab(driver: BrowserType, tab: FRONT_PAGE_TAB):
	if tab == FRONT_PAGE_TAB.CARS:
		driver.get(update_url(BASE_URL, category="osobowe"))
	elif tab == FRONT_PAGE_TAB.PARTS:
		driver.get(update_url(BASE_URL, category="czesci"))


def get_input_field_by_placeholder(driver: BrowserType, *, placeholder_text: str, switch_tab: FRONT_PAGE_TAB = None):
	if switch_tab is not None:
		switch_category_tab(driver, switch_tab)
	result = Inputs(driver).attr_filter('placeholder', placeholder_text)
	assert len(result) > 0
	return list(result.values())[0]


def get_car_brands_input_field(driver: BrowserType, *, switch_tab: bool = True) -> WebElement:
	return get_input_field_by_placeholder(driver, placeholder_text='Marka', switch_tab=FRONT_PAGE_TAB.CARS if switch_tab else None)


def get_car_model_input_field(driver: BrowserType, *, switch_tab: bool = True) -> WebElement:
	return get_input_field_by_placeholder(driver, placeholder_text='Model', switch_tab=FRONT_PAGE_TAB.CARS if switch_tab else None)


def get_car_generation_input_field(driver: BrowserType, *, switch_tab: bool = True) -> WebElement:
	return get_input_field_by_placeholder(driver, placeholder_text='Generacja', switch_tab=FRONT_PAGE_TAB.CARS if switch_tab else None)


def get_avaiable_car_brands(driver: BrowserType) -> Dict[str, int]:
	safely_click(get_car_brands_input_field(driver))
	car_brands = list(Spans(driver, By.XPATH, "//*[starts-with(@id, 'downshift-1-item-')]/div/span").content_dictionary().keys())
	return dict(sorted([split_name_amount(x) for x in car_brands], key=lambda x: x[1], reverse=True))


def get_avaiable_car_models(driver: BrowserType, brand: str) -> Dict[str, int]:
	safely_fill_input(get_car_brands_input_field(driver), brand)
	safely_click(get_car_model_input_field(driver, switch_tab=False))
	car_models = list(Spans(driver, By.XPATH, "//*[starts-with(@id, 'downshift-2-item-')]/div/span").content_dictionary().keys())
	return dict(sorted([split_name_amount(x) for x in car_models], key=lambda x: x[1], reverse=True))


def get_avaiable_car_generations(driver: BrowserType, brand: str, model: str) -> Dict[str, int]:
	safely_fill_input(get_car_brands_input_field(driver), brand)
	safely_fill_input(get_car_model_input_field(driver, switch_tab=False), model)
	safely_click(get_car_generation_input_field(driver, switch_tab=False))
	car_models = list(Spans(driver, By.XPATH, "//*[starts-with(@id, 'downshift-3-item-')]/div/span").content_dictionary().keys())
	return dict(sorted([split_name_amount_with_date_ranges(x) for x in car_models], key=lambda x: x[1], reverse=True))
