from pytest import fixture
from scrapper.server.browser_pool import get_backend

from tests.utils import Cars


@fixture(scope='module')
def api() -> str:
	try:
		yield str()
	finally:
		get_backend(quit=True)


@fixture
def cars_api(api : str) -> Cars:
	return Cars(api)
