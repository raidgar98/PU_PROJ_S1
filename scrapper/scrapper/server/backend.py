from threading import Lock, Semaphore, current_thread
from typing import Dict, Union

from scrapper.types import BrowserType, verify_types


class BrowserInstance:
	def __init__(self):
		self.__set_driver()
		self.__cache = dict()

	def __set_driver(self):
		self.__driver = BrowserType()

	def finish(self):
		self.__driver.quit()

	# cars
	def get_car_brands(self): pass
	def get_car_models(self, brand : str): pass
	def get_car_generations(self, brand : str, model : str): pass
	def list_cars(self, brand : str, model : str, generation : str): pass
	def get_car(self, link : str): pass

	# parts
	def get_part_brands(self): pass
	def get_part_categories(self, brand : str): pass
	def get_part_subcategories(self, brand : str, category : str): pass
	def list_parts(self, brand : str, category : str, subcategory : str): pass
	def get_part(self, link : str): pass

@verify_types()
def get_backend(*, quit : bool = False) -> Union[BrowserInstance, None]:

	class PoolSingleton:
		"""
		Carries handles for opened browsers
		"""

		MAX = 10
		__instances : Dict[int, BrowserInstance] = dict()
		__instance_lock = Semaphore(MAX)
		__write_lock = Lock()

		def __init__(self, write : bool = False):
			if write:
				self.count = PoolSingleton.MAX
				PoolSingleton.__write_lock.acquire(blocking=True)
			else:
				self.count = 1

		def __enter__(self) -> Dict[int, BrowserInstance]:
			for i in range(self.count):
				PoolSingleton.__instance_lock.acquire()
			return PoolSingleton.__instances

		def __exit__(self):
			PoolSingleton.__instance_lock.release(self.count)
			if self.count == PoolSingleton.MAX:
				PoolSingleton.__write_lock.release()

	if quit:
		with PoolSingleton(write=True) as instances:
			for _, browser in instances.items():
				browser.finish()
			return instances.clear() # return None

	# check is current thread is registered
	thread_id = current_thread().native_id
	with PoolSingleton() as instances:
		result =  instances.get(thread_id)
		if result is not None:
			return result

	# if not returned, add missing browser, for current thread
	with PoolSingleton(write=True) as instances:
		instances[thread_id] = BrowserInstance()
		return instances[thread_id]
