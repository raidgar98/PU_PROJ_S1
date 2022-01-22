from typing import List
from scrapper.pages.accessors.car_list import validate_car_offers_page
from scrapper.utilities.presets import Links, OfferLinks, Spans
from scrapper.utilities.common import is_offer_link, pagination_dto
from scrapper.utilities.url_param_extender import update_url
from selenium.webdriver.common.by import By
from scrapper.types import BrowserType

def validate_part_offers_page(driver : BrowserType):
	assert '/czesci' in driver.current_url

def get_parts_offers(driver : BrowserType) -> List[str]:
	return list(Links(driver).href_dict(lambda x : is_offer_link(x[0])).keys())

def get_parts_offers_with_max_page_num(driver : BrowserType, query: str, price_to : int, price_from : int, page : int) -> pagination_dto:
	olh = OfferLinks(driver, validation_function=validate_part_offers_page)
	olh.set_page(page)
	olh.set_prices(price_from, price_to)
	olh.update_url('q-' + query.replace(' ', '-'))
	return olh.retrive()
