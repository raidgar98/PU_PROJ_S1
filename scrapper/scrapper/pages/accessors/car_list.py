from typing import List

from scrapper.conf import BASE_URL
from scrapper.utilities.common import is_offer_link, pagination_dto
from scrapper.types import BrowserType
from scrapper.utilities.presets import Links, OfferLinks, Spans
from scrapper.utilities.url_param_extender import update_url
from selenium.webdriver.common.by import By



class list_cars_dto(object):
	def __init__(self, urls : List[str], max_page_num : int):
		self.urls = urls
		self.max_page_num = max_page_num if isinstance(max_page_num, int) else int(max_page_num)

def validate_car_offers_page(driver : BrowserType):
	assert '?category=osobowe' in driver.current_url or '/osobowe' in driver.current_url, f'not found osobowe in {driver.current_url}'

def get_cars_offers_with_max_page_num(driver : BrowserType, price_to : int, price_from : int = 0, page : int = None) -> pagination_dto:
	olh = OfferLinks(driver, validation_function=validate_car_offers_page)
	olh.set_page(page)
	olh.set_prices(price_from, price_to)
	olh.update_url(**{
			"search[filter_enum_damaged]":1
		}
	)
	return olh.retrive()
