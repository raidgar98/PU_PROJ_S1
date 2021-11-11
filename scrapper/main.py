#!/usr/bin/python3


from json import dump
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


def get_driver():
	# options = Options()
	# options.set_preference('javascript.enabled', False)
	return webdriver.Chrome('/usr/bin/chromedriver')
	# return webdriver.Firefox(options=options)


driver = get_driver()
try:
	driver.get('https://www.otomoto.pl/')

	cookie_banner : WebElement = driver.find_element(By.ID, "onetrust-accept-btn-handler")
	cookie_banner.click()

	a_tags : List[WebElement] = driver.find_elements(By.TAG_NAME, 'a')
	a_href = [ x.get_attribute('href') for x in a_tags ]
	catgories = set(filter(lambda x: 'category' in x and 'czesci' in x, a_href))
	print(catgories)
	catgories = list(catgories)
	assert len(catgories) == 1

	# wyszukanie zaawansowane
	driver.get(catgories[0])
	element : WebElement = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[2]/article/fieldset/div/form/div[2]/button[2]')
	element.send_keys(Keys.ENTER)

	# table of contents
	driver.implicitly_wait(3)
	table_of_contents = driver.find_elements(By.CLASS_NAME, "ds-tree")
	print(f'znaleziono: {len(table_of_contents)} elementów')
	# table_of_contents = driver.find_elements(By.XPATH, "/html/body/div[4]/div[3]/section/div/div[2]/aside/div[1]/div/div[2]/div/ul/li/ul/button/a/span[@class='ds-tree-node-child']")
	print(table_of_contents)
	table_of_contents = [x.text for x in table_of_contents][0].splitlines()
	print(table_of_contents)
	# input()

	with open('categories.json', 'wt') as file:
		dump( [ x.split('(')[0] for x in table_of_contents ], file, ensure_ascii=False)
except:
	pass
finally:
	driver.quit()