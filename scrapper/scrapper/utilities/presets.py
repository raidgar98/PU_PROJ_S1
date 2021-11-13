from typing import Callable, Dict, List, Union

from selenium.webdriver.remote.webelement import WebElement

from scrapper.types import BrowserType, By
from scrapper.utilities.common import attribiute_dictionary, element_dictionary, filter_attribiute_dictionary, find_elements


class Preset:
	"""
	presets are helper classes that automates process of finding specific types on web page
	"""
	def __init__(self, driver: BrowserType, by: By, search: str):
		"""
		[protected] inititalizes preset

		:param driver: driver to use
		:type driver: BrowserType
		:param by: filter type
		:type by: By
		:param search: filter query
		:type search: str
		"""
		self.driver = driver
		self.by = by
		self.search = search

	def find(self) -> List[WebElement]:
		"""
		finds WebElements of preset type

		:rtype: List[WebElement]
		"""
		return find_elements(self.driver, self.by, self.search)


class Links(Preset):
	"""
	represents <a href=""> tags
	"""
	def __init__(self, driver: BrowserType):
		super().__init__(driver, By.TAG_NAME, 'a')
		self.attr = 'href'

	def href_dict(self) -> Dict[str, WebElement]:
		"""
		returns map of links->WebElement

		:rtype: Dict[str, WebElement]
		"""
		return attribiute_dictionary(self.driver, self.by, self.search, self.attr)

	def href_dict(self, filter: Union[Callable, str]) -> Dict[str, WebElement]:
		"""
		returns filtered map of links->WebElement

		:param filter: function to use while filtering
		:type filter: Union[Callable, str]
		:rtype: Dict[str, WebElement]
		"""
		return filter_attribiute_dictionary(self.driver, self.by, self.search, self.attr, filter)


class Buttons(Preset):
	"""
	represents <button> tag
	"""
	def __init__(self, driver: BrowserType):
		super().__init__(driver, By.TAG_NAME, 'button')

	def attr_filter(self, attr: str, filter: Union[Callable, str]) -> Dict[str, WebElement]:
		"""
		returns filtered map by any button tag attribute

		:param attr: value under this attr. will be used as a key
		:type attr: str
		:param filter: function to use while filtering
		:type filter: Union[Callable, str]
		:rtype: Dict[str, WebElement]
		"""
		return filter_attribiute_dictionary(self.driver, self.by, self.search, attr, filter)


class Inputs(Buttons):
	"""
	represents <input> tag

	:note Buttons: it shares simillar functionalities, there is no logical connection
	"""
	def __init__(self, driver: BrowserType):
		super().__init__(driver)
		self.search = 'input'


class Spans(Preset):
	"""
	represents <span> tag
	"""
	def __init__(self, driver, by: By = By.TAG_NAME, search: str = 'span'):
		super().__init__(driver, by, search)

	def content_dictionary(self) -> Dict[str, WebElement]:
		"""
		returns map of span_content -> WebElement

		:rtype: Dict[str, WebElement]
		"""
		return element_dictionary(self.driver, self.by, self.search, lambda x: x.text)
