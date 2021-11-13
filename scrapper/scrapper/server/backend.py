from scrapper.conf import get_logger
from scrapper.types import BrowserType

log = get_logger()



class BrowserInstance:
	def __init__(self):
		self.__set_driver()
		self.__cache = dict()

	def __set_driver(self):
		self.__driver = BrowserType()
		log.debug(f'creating new `{type(self.__driver).__name__}` instance!')

	def finish(self):
		self.__driver.quit()

	# cars
	def get_car_brands(self): pass
	def get_car_models(self, brand: str): pass
	def get_car_generations(self, brand: str, model: str): pass
	def list_cars(self, brand: str, model: str, generation: str): pass
	def get_car(self, link: str): pass

	# parts
	def get_part_brands(self): pass
	def get_part_categories(self, brand: str): pass
	def get_part_subcategories(self, brand: str, category: str): pass
	def list_parts(self, brand: str, category: str, subcategory: str): pass
	def get_part(self, link: str): pass
