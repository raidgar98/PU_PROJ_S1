from os import environ

from scrapper.conf import get_logger
from scrapper.pages.accessors.car_list import (		get_cars_offers,
																	get_cars_offers_with_max_page_num)
from scrapper.pages.accessors.front_page import (	get_avaiable_car_brands,
																	get_avaiable_car_generations,
																	get_avaiable_car_models,
																	goto_car_list_offers,
																	goto_front_page,
																	try_accept_cookies)
from scrapper.types import BrowserType, BrowserOptionsType

log = get_logger()

def cache():
	def cache_impl(fun):
		def cache_impl_impl(*args, **kwargs):
			that: BrowserInstance = args[0]  # self
			arg_hash = fun.__name__
			if len(args) > 1 or len(kwargs) > 0:
				arg_hash = ' '.join(args[1:])
				arg_hash += ' '.join(list(kwargs.values()))
			result = that.get_from_cache(arg_hash)
			if result is not None:
				return result
			else:
				result = fun(*args, **kwargs)
				that.add_to_cache(arg_hash, result)
				return result
		return cache_impl_impl
	return cache_impl


class BrowserInstance:
	def __init__(self):
		self.__browser_options : BrowserOptionsType = None
		self.__set_driver()
		self.__cache = dict()

	def __set_driver(self):
		if environ.get('HEADLESS', False):
			self.__browser_options = BrowserOptionsType()
			self.__browser_options.add_argument("--headless")
			self.__browser_options.add_argument("--no-sandbox")
		self.__driver = BrowserType(options=self.__browser_options)

		log.debug(f'creating new `{type(self.__driver).__name__}` instance!')
		goto_front_page(self.__driver)
		try_accept_cookies(self.__driver)

	def finish(self):
		self.__driver.quit()

	def add_to_cache(self, key, value):
		self.__cache[key] = value

	def get_from_cache(self, key):
		return self.__cache.get(key, None)

	# cars
	@cache()
	def get_car_brands(self):
		return get_avaiable_car_brands(self.__driver)

	@cache()
	def get_car_models(self, brand: str):
		return get_avaiable_car_models(self.__driver, brand)

	@cache()
	def get_car_generations(self, brand: str, model: str):
		return get_avaiable_car_generations(self.__driver, brand, model)

	def list_cars(self, brand: str, model: str, generation: str, price_to : int, price_from : int = 0, page : int = None):
		goto_car_list_offers(self.__driver, brand, model, generation)
		return get_cars_offers_with_max_page_num(driver=self.__driver, price_to=price_to, price_from=price_from, page=page)

	def get_car(self, link: str): pass

	# parts
	def get_part_brands(self): pass
	def get_part_categories(self, brand: str): pass
	def get_part_subcategories(self, brand: str, category: str): pass
	def list_parts(self, brand: str, category: str, subcategory: str): pass
	def get_part(self, link: str): pass
