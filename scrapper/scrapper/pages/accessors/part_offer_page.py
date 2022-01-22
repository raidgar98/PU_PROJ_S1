from typing import Dict

from selenium.webdriver.common.by import By
from scrapper.pages.accessors.front_page import get_part_brands_input_field
from scrapper.utilities.common import safely_click, split_name_amount
from scrapper.utilities.presets import Spans
from scrapper.types import BrowserType


