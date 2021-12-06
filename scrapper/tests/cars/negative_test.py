from tests.utils import Cars

def test_get_model_invalid_brand(cars_api : Cars):
	assert len(cars_api.get_models(brand='aaaaaaaaaaaaaaaaaaaaaaaa')) == 0

def test_get_generation_invalid_model(cars_api : Cars):
	assert len(cars_api.get_generations(brand='Opel', model='bbbbbbbbbbbbbbb')) == 0


