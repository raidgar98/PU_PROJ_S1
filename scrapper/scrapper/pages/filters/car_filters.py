from time import sleep
from types import FunctionType
from typing import List

from scrapper.conf import BASE_URL
from scrapper.pages.accessors.front_page import get_car_brands_input_field, get_car_generation_input_field, get_car_model_input_field
from scrapper.types import BrowserType, not_empty, verify_types
from scrapper.utilities.common import safely_click, safely_fill_input
from scrapper.utilities.presets import Buttons, Inputs
from scrapper.utilities.url_param_extender import update_url
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


@verify_types(car_brand=not_empty, car_model=not_empty)
def setup_car_filters_impl(*, driver: BrowserType, car_brand: str, car_model: str, car_generation: str = None, **url_params) -> None:

	# fill proper inputs
	safely_fill_input(get_car_brands_input_field(driver), car_brand)
	safely_fill_input(get_car_model_input_field(driver, switch_tab=False), car_model)
	if car_generation is not None:
		safely_fill_input(get_car_generation_input_field(driver, switch_tab=False), car_generation)

	# get submit button
	buttons = Buttons(driver).attr_filter('data-testid', 'submit-btn')
	assert len(buttons) == 1
	safely_click(buttons[0])

	# add to current url additional parameters
	if len(url_params) > 0:
		url = update_url(driver.current_url, **url_params)

	# apply filter (submit)
	driver.get(url)
