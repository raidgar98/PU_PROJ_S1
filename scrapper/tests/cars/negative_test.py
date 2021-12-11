from tests.utils import Cars
from pytest import raises

def test_get_model_invalid_brand(cars_api : Cars):
	assert len(cars_api.get_models(brand='aaaaaaaaaaaaaaaaaaaaaaaa')) == 0

def test_get_generation_invalid_model(cars_api : Cars):
	assert len(cars_api.get_generations(brand='Opel', model='bbbbbbbbbbbbbbb')) == 0

def test_list_cars_negative_value(cars_api : Cars):
	with raises(AssertionError):
		cars_api.list(brand='', model='', price_to=-1)
