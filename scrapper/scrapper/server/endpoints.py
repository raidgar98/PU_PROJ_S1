from typing import List
from jsonrpcserver.methods import Methods

from scrapper.scrapper.server.backend import BrowserInstance

def get_brands(ctx : BrowserInstance) -> List[str]:
	return ctx.get_car_brands()



def build_methods() -> Methods:
	result = Methods()
	result.add()
