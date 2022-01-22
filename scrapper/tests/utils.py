import json
from os import getpid
from scrapper.server.endpoints import build_methods

from scrapper.server.engine import Handler

def prepare_jsonrpc(method, params) -> dict:
	return {
		"id": getpid(),
		"jsonrpc": "2.0",
		"method": method,
		"params": params
	}

class Api:
	def __init__(self, url : str, prefix : str):
		self.url = url
		self.prefix = prefix

	def send(self, endpoint, **params) -> str:
		return Handler.perform_dispatch(json.dumps(prepare_jsonrpc(f'{self.prefix}.{endpoint}', params)), build_methods())

def endpoint():
	def endpoint_impl(foo):
		def endpoint_impl_args(that, **kwargs) -> dict:
			res =  json.loads(that.send(foo.__name__, **kwargs))
			assert not 'error' in res
			return res['result']
		return endpoint_impl_args
	return endpoint_impl

class Cars(Api):
	def __init__(self, url : str):
		super().__init__(url, 'cars')

	@endpoint()
	def brands(self) -> dict : pass

	@endpoint()
	def models(self, *, brand : str) -> dict : pass

	@endpoint()
	def generations(self, *, brand : str, model : str) -> dict : pass

	@endpoint()
	def list(self, *, brand: str, model: str, price_to : int, price_from : int = 0, generation : str = None, page : int = None) -> dict : pass
