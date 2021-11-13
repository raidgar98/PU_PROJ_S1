from scrapper.types import BrowserType
from .car_filters import setup_car_filters_impl


def setup_car_filters(*, driver: BrowserType, car_brand: str, car_model: str, car_generation: str = None, **url_params) -> None:
	"""
	Using given driver, fills form on page that allows filtering cars and clicks search button

	:param driver: this driver will be used for actions
	:type driver: BrowserType
	:param car_brand: brand of a car to put in a text box
	:type car_brand: str
	:param car_model: model of car to put in a text box
	:type car_model: str
	:param car_generation: generation of cat to put in a text box, defaults to None
	:type car_generation: str, optional

	:return: nothing
	"""
	return setup_car_filters_impl(driver=driver, car_brand=car_brand, car_model=car_model, car_generation=car_generation, **url_params)
