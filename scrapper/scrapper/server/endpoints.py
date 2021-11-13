from typing import List

from jsonrpcserver import Success
from jsonrpcserver.methods import Methods
from scrapper.server.backend import BrowserInstance
from scrapper.types import verify_types


@verify_types()
def get_brands(ctx: BrowserInstance) -> List[str]:
	return Success({"brands": ctx.get_car_brands()})


def build_methods() -> Methods:
	return {
		"cars.get_brands": get_brands
	}
