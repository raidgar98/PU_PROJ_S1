from scrapper.conf import get_logger
from scrapper.types import BrowserType
from scrapper.pages.accessors.front_page import get_avaiable_car_brands, get_avaiable_car_models, get_avaiable_car_generations, try_accept_cookies, goto_front_page

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
		self.__set_driver()
		self.__cache = dict()

	def __set_driver(self):
		self.__driver = BrowserType()
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

	def list_cars(self, brand: str, model: str, generation: str): pass
	def get_car(self, link: str): pass

	# parts
	def get_part_brands(self): pass
	def get_part_categories(self, brand: str): pass
	def get_part_subcategories(self, brand: str, category: str): pass
	def list_parts(self, brand: str, category: str, subcategory: str): pass
	def get_part(self, link: str): pass
