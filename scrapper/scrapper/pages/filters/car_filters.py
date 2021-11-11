from time import sleep
from types import FunctionType
from typing import List

from scrapper import BASE_URL
from scrapper.types import BrowserType, not_empty, verify_types
from scrapper.utilities.url_param_extender import update_url
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


@verify_types(car_brand=not_empty, car_model=not_empty)
def setup_car_filters_impl(*, driver : BrowserType, car_brand : str, car_model : str, car_generation : str = None, **url_params) -> None:
	PLACEHOLDER = 'placeholder'		# placeholder caption
	INPUT_FIELDS_PLACEHOLDERS = {		# unique strings to find on page
		'Marka pojazdu': car_brand,
		'Model pojazdu': car_model,
		'Generacja': car_generation
	}

	if driver.current_url != BASE_URL:
		driver.get(BASE_URL)

	# iterate over found text inputs
	for input_element in find_matching_elements(driver, 'input', lambda x: x.get_attribute(PLACEHOLDER) in INPUT_FIELDS_PLACEHOLDERS):
		placeholder = INPUT_FIELDS_PLACEHOLDERS[input_element.get_attribute(PLACEHOLDER)]
		if placeholder is not None:
			input_element.send_keys( placeholder )
			input_element.send_keys( Keys.ENTER )		# if not send, page will not activate next field
			sleep(1)

	# find matching button
	buttons = find_matching_elements(driver, 'button', lambda x: x.get_attribute('data-testid') == 'submit-btn')
	assert len(buttons) == 1
	buttons[0].click()
	sleep(1)

	# add to current url additional parameters
	if len(url_params) > 0:
		url = update_url(driver.current_url, **url_params)
		driver.get(url)

def find_matching_elements(driver : BrowserType, tag_name : str, filter : FunctionType) -> List[WebElement]:
	elements = driver.find_elements(By.TAG_NAME, tag_name)
	return [ element for element in elements if filter(element) ]
