from typing import Callable, Union

from scrapper.types import BrowserType, By
from scrapper.utilities.common import attribiute_dictionary, element_dictionary, filter_attribiute_dictionary, find_elements


class Preset:
	def __init__(self, driver: BrowserType, by: By, search: str):
		self.driver = driver
		self.by = by
		self.search = search

	def find(self):
		return find_elements(self.driver, self.by, self.search)


class Links(Preset):
	def __init__(self, driver: BrowserType):
		super().__init__(driver, By.TAG_NAME, 'a')
		self.attr = 'href'

	def href_dict(self):
		return attribiute_dictionary(self.driver, self.by, self.search, self.attr)

	def href_dict(self, filter: Union[Callable, str]):
		return filter_attribiute_dictionary(self.driver, self.by, self.search, self.attr, filter)


class Buttons(Preset):
	def __init__(self, driver: BrowserType):
		super().__init__(driver, By.TAG_NAME, 'button')

	def attr_filter(self, attr: str, filter: Union[Callable, str]):
		return filter_attribiute_dictionary(self.driver, self.by, self.search, attr, filter)


class Inputs(Buttons):
	def __init__(self, driver: BrowserType):
		super().__init__(driver)
		self.search = 'input'


class Spans(Preset):
	def __init__(self, driver, by: By = By.TAG_NAME, search: str = 'span'):
		super().__init__(driver, by, search)

	def content_dictionary(self):
		return element_dictionary(self.driver, self.by, self.search, lambda x: x.text)
