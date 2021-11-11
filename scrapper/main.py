#!/usr/bin/python3

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from scrapper import BASE_URL
from scrapper.types import BrowserType
from scrapper.pages.filters import setup_car_filters

def get_driver():
	return BrowserType()

URL_PARAMS = {
	"path": ['sosnowiec'],
	"search[dist]": 50
}

driver = get_driver()
try:
	driver.get(BASE_URL)

	# accept cookies
	cookie_banner : WebElement = driver.find_element(By.ID, "onetrust-accept-btn-handler")
	cookie_banner.click()

	# setup filters
	setup_car_filters(driver=driver, car_brand='Opel', car_model='Astra', **URL_PARAMS)

	input()

finally:
	driver.quit()
