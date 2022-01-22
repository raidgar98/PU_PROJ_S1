from pyclbr import Function
from re import compile
from typing import Callable, Dict, List, Union
from scrapper.utilities.url_param_extender import update_url

from scrapper.types import BrowserType, By
from scrapper.utilities.common import (attribiute_dictionary,
													element_dictionary,
													filter_attribiute_dictionary,
													find_elements, is_offer_link, pagination_dto)
from selenium.webdriver.common import by
from selenium.webdriver.remote.webelement import WebElement


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

	def caption_dict(self, query : str) -> Dict[str, WebElement]:
		regex = compile(query)
		return dict(filter(lambda x : regex.search(x[0]) is not None, element_dictionary(self.driver, self.by, self.search, lambda x : x.text).items()))

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
	def __init__(self, driver : BrowserType, by: By = By.TAG_NAME, search: str = 'span'):
		super().__init__(driver, by, search)

	def content_dictionary(self) -> Dict[str, WebElement]:
		"""
		returns map of span_content -> WebElement

		:rtype: Dict[str, WebElement]
		"""
		return element_dictionary(self.driver, self.by, self.search, lambda x: x.text)


class OfferLinks():
	"""
	represents links from searchg result page
	"""

	def __init__(self, driver : BrowserType, *, validation_function : Function = lambda _ : True):
		self.__driver = driver
		validation_function(self.__driver)
		self.url = self.__driver.current_url

	def update_url(self, *path, **params):
		self.url = update_url(self.url, path=path, **params)

	def set_prices(self, price_from : int, price_to : int):
		self.update_url(
			**{
				"search[filter_float_price:to]":price_to,
				"search[filter_float_price:from]":price_from,
			}
		)

	def set_page(self, num : int):
		self.update_url(page=(1 if num is None else num))

	def __get_offers(self) -> List[str]:
		return list(Links(self.__driver).href_dict(lambda x : is_offer_link(x[0])).keys())

	def retrive(self) -> pagination_dto:
		self.__driver.get(self.url)
		links = self.__get_offers()

		max_page_num = 1
		page_spans = list(Spans(self.__driver, By.XPATH, '//*[@id="body-container"]/div[2]/div[2]/ul/li/a/span[contains(@class,"page")]').content_dictionary().keys())
		page_spans.extend( Spans(self.__driver, By.XPATH, '//*[@id="body-container"]/div[2]/div[2]/ul/li[@class="active"]').content_dictionary().keys() )
		if len(page_spans):
			max_page_num = max(page_spans, key=lambda x: int(x) if x is not None and '...'not in x else 0)

		return pagination_dto(links, max_page_num)

