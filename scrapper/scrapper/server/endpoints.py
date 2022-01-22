from typing import Any, Dict, List

from jsonrpcserver import Success
from jsonrpcserver.methods import Methods
from scrapper.server.backend import BrowserInstance
from scrapper.types import Param, verify_types

def unsigned(x : Param):
	assert x.value >= 0

@verify_types()
def get_car_brands(ctx: BrowserInstance) -> List[str]:
	return Success(ctx.get_car_brands())


@verify_types()
def get_car_models(ctx: BrowserInstance, *, brand: str) -> List[str]:
	return Success(ctx.get_car_models(brand=brand))


@verify_types()
def get_car_generations(ctx: BrowserInstance, *, brand: str, model: str) -> List[str]:
	return Success(ctx.get_car_generations(brand=brand, model=model))

@verify_types(page=unsigned, price_from=unsigned, price_to=unsigned)
def list_car_offers(ctx: BrowserInstance, *, brand: str, model: str, price_to : int, price_from : int = 0, generation : str = None, page : int = None) -> List[str]:
	return Success(ctx.list_cars(brand=brand, model=model, generation=generation, price_to=price_to, price_from=price_from, page=page))

@verify_types()
def offer_details(ctx: BrowserInstance, *, link : str) -> Dict[str, Any]:
	return Success(ctx.get_car(link=link))

@verify_types()
def offer_images(ctx: BrowserInstance, *, link : str) -> List[str]:
	return Success(ctx.get_car_images(link=link))

def build_methods() -> Methods:
	return {
		# cars
		"cars.brands": get_car_brands,
		"cars.models": get_car_models,
		"cars.generations": get_car_generations,
		"cars.list": list_car_offers,
		"cars.detail": car_offer_details,
		"cars.images": car_offer_images,
	}
