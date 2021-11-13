from functools import partial
from re import compile
from re import match as regex_match
from re import search as regex_search
from time import sleep
from types import LambdaType
from typing import Any, Callable, Dict, List, Match, Tuple, Union

from scrapper.conf import get_logger
from scrapper.types import BrowserType
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

log = get_logger()

def find_elements(driver: BrowserType, by: By, search: str) -> List[WebElement]:
	return driver.find_elements(by, search)


def element_dictionary(driver: BrowserType, by: By, search: str, key_foo: LambdaType) -> Dict[Any, WebElement]:
	return {key_foo(x): x for x in find_elements(driver, by, search)}


def attribiute_dictionary(driver: BrowserType, by: By, search: str, attr: str) -> Dict[str, WebElement]:
	return element_dictionary(driver, by, search, lambda x: x.get_attribute(attr))


def filter_attribiute_dictionary(driver: BrowserType, by: By, search: str, attr: str, filter_input: Union[Callable, str]):
	if isinstance(filter_input, str):
		compiled_regex = compile(filter_input)

		def filter_foo(x: Tuple[str, WebElement]):
			return regex_search(compiled_regex, x[0])
	else:
		filter_foo = filter_input
	return dict(filter(filter_foo, attribiute_dictionary(driver, by, search, attr).items()))


def safely_fill_input(element: WebElement, text: str, *, requires_confirmation: bool = True):
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
	assert element is not None
	element.click()
	sleep(1)


def split_name_amount(line: str):
	splitted = line.strip().rsplit('(')
	return splitted[0].strip(), int(splitted[1].strip('()'))


def split_name_amount_with_date_ranges(line: str):
	result: Match = regex_match('([A-Za-z0-9]+) \(([0-9]+-([0-9]+)?)\) \(([0-9]+)\)', line)
	return f'{result.group(1)} ({result.group(2)})', result.group(4)
