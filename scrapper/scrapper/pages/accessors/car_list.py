from typing import List

from scrapper.conf import BASE_URL
from scrapper.utilities.presets import Links, Spans
from scrapper.utilities.url_param_extender import update_url
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

def is_car_offer_link(x : str):
	return \
		x is not None and \
		x.startswith(BASE_URL) and \
		'/oferta/' in x and \
		not 'finansowanie.otomoto.pl' in x

class list_cars_dto(object):
	def __init__(self, urls : List[str], max_page_num : int):
		self.urls = urls
		self.max_page_num = max_page_num if isinstance(max_page_num, int) else int(max_page_num)

def validate_car_offers_page(driver : WebDriver):
	pass
	# assert '/osobowe' in driver.current_url

def get_cars_offers(driver : WebDriver) -> List[str]:


	return list(Links(driver).href_dict(lambda x : is_car_offer_link(x[0])).keys())

def get_cars_offers_with_max_page_num(driver : WebDriver, price_to : int, price_from : int = 0, page : int = None) -> list_cars_dto:
	validate_car_offers_page(driver)
	if page is None:
		page = 1

	updated_url = update_url(driver.current_url, **{
			"search[filter_enum_damaged]":1,
			"search[filter_float_price:to]":price_to,
			"search[filter_float_price:from]":price_from,
			"page": page
		}
	)
	driver.get(updated_url)
	links = get_cars_offers(driver)
	max_page_num = 1
	page_spans = list(Spans(driver, By.XPATH, '//*[@id="body-container"]/div[2]/div[2]/ul/li/a/span[contains(@class,"page")]').content_dictionary().keys())
	page_spans.extend( Spans(driver, By.XPATH, '//*[@id="body-container"]/div[2]/div[2]/ul/li[@class="active"]').content_dictionary().keys() )
	if len(page_spans):
		max_page_num = max(page_spans, key=lambda x: int(x) if x is not None and '...'not in x else 0)
	return list_cars_dto(links, max_page_num)
