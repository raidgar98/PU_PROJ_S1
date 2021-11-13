from typing import List

from jsonrpcserver import Success
from jsonrpcserver.methods import Methods
from scrapper.server.backend import BrowserInstance
from scrapper.types import verify_types


@verify_types()
def get_car_brands(ctx: BrowserInstance) -> List[str]:
	return Success(ctx.get_car_brands())


@verify_types()
def get_car_models(ctx: BrowserInstance, *, brand: str) -> List[str]:
	return Success(ctx.get_car_models(brand=brand))


@verify_types()
def get_car_generations(ctx: BrowserInstance, *, brand: str, model: str) -> List[str]:
	return Success(ctx.get_car_generations(brand=brand, model=model))


def build_methods() -> Methods:
	return {
		"cars.get_brands": get_car_brands,
		"cars.get_models": get_car_models,
		"cars.get_generations": get_car_generations,
	}
