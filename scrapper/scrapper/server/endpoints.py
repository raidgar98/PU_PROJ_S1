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
def car_offer_details(ctx: BrowserInstance, *, link : str) -> Dict[str, Any]:
	return Success(ctx.get_car(link=link))

@verify_types()
def car_offer_images(ctx: BrowserInstance, *, link : str) -> List[str]:
	return Success(ctx.get_car_images(link=link))

@verify_types()
def get_part_brands(ctx: BrowserInstance):
	return Success(ctx.get_part_brands())

@verify_types()
def list_part_offers(ctx: BrowserInstance, *, query : str, price_to : int = 50_000, price_from : int = 0, brand : str = None, page : int = None) -> List[str]:
	return Success(ctx.list_parts(query=query, brand=brand, price_to=price_to, price_from=price_from, page=page))

@verify_types()
def parts_offer_details(ctx: BrowserInstance, *, link : str) -> Dict[str, Any]:
	return Success(ctx.get_part(link=link))

@verify_types()
def parts_offer_images(ctx: BrowserInstance, *, link : str) -> List[str]:
	return Success(ctx.get_part_images(link=link))



def build_methods() -> Methods:
	return {
		# cars
		"cars.brands": get_car_brands,
		"cars.models": get_car_models,
		"cars.generations": get_car_generations,
		"cars.list": list_car_offers,
		"cars.detail": car_offer_details,
		"cars.images": car_offer_images,

		# parts
		"parts.brands": get_part_brands,
		"parts.query": list_part_offers,
		"parts.detail": parts_offer_details,
		"parts.images": parts_offer_images
	}
