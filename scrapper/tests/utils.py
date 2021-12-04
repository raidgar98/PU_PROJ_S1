from requests import post as send_post
from os import getpid

def send(url : str, data : dict) -> str:
	result = send_post(url, json=data)

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

	def send(self, endpoint, **params) -> dict:
		return send(self.url, prepare_jsonrpc(f'{self.prefix}.{endpoint}', params))

def endpoint():
	def endpoint_impl(foo):
		def endpoint_impl_args(that, **kwargs) -> dict:
			return that.send(foo.__name__, **kwargs)
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
	def page_list(self, *, brand: str, model: str, price_to : int, price_from : int = 0, generation : str = None, page : int = None) -> dict : pass




