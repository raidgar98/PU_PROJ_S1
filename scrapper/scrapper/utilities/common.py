from functools import partial
from re import compile
from re import match as regex_match
from re import search as regex_search
from time import sleep
from types import LambdaType
from typing import Any, Callable, Dict, List, Match, Tuple, Union

from scrapper.conf import BASE_URL, get_logger
from scrapper.types import BrowserType
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

log = get_logger()

class pagination_dto(object):
	def __init__(self, urls : List[str], max_page_num : int):
		self.urls = urls
		self.max_page_num = max_page_num if isinstance(max_page_num, int) else int(max_page_num)

def find_elements(driver: BrowserType, by: By, search: str) -> List[WebElement]:
	"""
	encapsulates driver.find_elements

	:param driver: driver to use
	:type driver: BrowserType
	:param by: filter type
	:type by: By
	:param search: filter query
	:type search: str
	:return: list of matched WebElements
	:rtype: List[WebElement]
	"""
	return driver.find_elements(by, search)


def element_dictionary(driver: BrowserType, by: By, search: str, key_foo: LambdaType) -> Dict[Any, WebElement]:
	"""
	associates output from processing of WebElement (by given lambda) to that WebElement. This is generic function

	:param driver: driver to use
	:type driver: BrowserType
	:param by: filter type
	:type by: By
	:param search: filter query
	:type search: str
	:param key_foo: output from this lambda will be used as key in dict, so it should be hashable
	:type key_foo: LambdaType
	:rtype: Dict[Any, WebElement]
	"""
	return {key_foo(x): x for x in find_elements(driver, by, search)}


def attribiute_dictionary(driver: BrowserType, by: By, search: str, attr: str) -> Dict[str, WebElement]:
	"""
	specialization of element_dictionary, where lambda returns given attribiute

	:param driver: driver to use
	:type driver: BrowserType
	:param by: filter type
	:type by: By
	:param search: filter query
	:type search: str
	:param attr: value under this attr. will be used as key in result dict
	:type attr: str
	:rtype: Dict[str, WebElement]
	"""
	return element_dictionary(driver, by, search, lambda x: x.get_attribute(attr))


def filter_attribiute_dictionary(driver: BrowserType, by: By, search: str, attr: str, filter_input: Union[Callable, str]) -> Dict[str, WebElement]:
	"""
	encapsulates attribiute_dictionary and additionally filters output

	:param driver: driver to use
	:type driver: BrowserType
	:param by: filter type
	:type by: By
	:param search: filter query
	:type search: str
	:param attr: value under this attr. will be used as key in result dict
	:type attr: str
	:param filter_input: str will be used as regex input
	:type filter_input: Union[Callable, str]
	:rtype: Dict[str, WebElement]
	"""
	if isinstance(filter_input, str):
		compiled_regex = compile(filter_input)

		def filter_foo(x: Tuple[str, WebElement]):
			return regex_search(compiled_regex, x[0])
	else:
		filter_foo = filter_input
	return dict(filter(filter_foo, attribiute_dictionary(driver, by, search, attr).items()))


def safely_fill_input(element: WebElement, text: str, *, requires_confirmation: bool = True):
	"""
	fills given WebElement as safe as it is possible (shouldn't throw exception)

	:param element: should be input field
	:type element: WebElement
	:param text: text to write
	:type text: str
	:param requires_confirmation: if set to False additonal confiramtion (ENTER) will not be performed, defaults to True
	:type requires_confirmation: bool, optional
	"""
	assert element is not None
	assert element.tag_name == 'input'

	try:
		element.send_keys(text)
	except ElementNotInteractableException:
		log.warning('exception occured when inserting text to input field')
	if requires_confirmation:
		try:
			element.send_keys(Keys.ENTER)
			sleep(0.5)
		except ElementNotInteractableException:
			log.warning('exception occured when confirming input')


def safely_click(element: WebElement):
	"""
	encapsulates clicking on button

	:param element: should be button
	:type element: WebElement
	"""
	assert element is not None
	element.click()
	sleep(1)


def split_name_amount(line: str) -> Tuple[str, int]:
	"""
	splits string

	:example: "Honda (2000)" -> ["Honda", 2000]
	:param line: text to process
	:type line: str
	:return: splitted line
	:rtype: Tuple[str, int]
	"""
	splitted = line.strip().rsplit('(')
	return splitted[0].strip(), int(splitted[1].strip('()'))


def split_name_amount_with_date_ranges(line: str) -> Tuple[str, int]:
	"""
	splits string

	:example: "Honda (2015-2019) (2000)" -> ["Honda (2015-2019)", 2000]
	:param line: text to process
	:type line: str
	:return: splitted line
	:rtype: Tuple[str, int]
	"""
	result: Match = regex_match('(.+) \(([0-9]+-([0-9]+)?)\) \(([0-9]+)\)', line)
	return f'{result.group(1)} ({result.group(2)})', result.group(4)


def is_offer_link(link : str) -> bool:
	"""
	verifies is given string a link to offer

	:param link: link to verify
	:type link: str
	:return: verify status
	:rtype: bool
	"""
	return \
		link is not None and \
		link.startswith(BASE_URL) and \
		'/oferta/' in link and \
		not 'finansowanie.otomoto.pl' in link # filters out ads

