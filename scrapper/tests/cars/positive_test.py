from tests.utils import Cars

REQUIRED_BRANDS = ['Audi', 'BMW', 'Opel', 'Ford', 'Syrena', 'Toyota', 'Alpine', 'Aro']
REQUIRED_MODELS = ["101", "102", "103", "104", "105", "Bosto", "Inny", "R-20"]
REQUIRED_GENERATIONS = ["I (1998-2002)","II (2003-2011)"]

def test_brands(cars_api : Cars):
	brands = list(cars_api.get_brands().keys())
	for brand in REQUIRED_BRANDS:
		assert brand in brands

def test_models(cars_api : Cars):
	models = list(cars_api.get_models(brand='Syrena').keys())
	for model in REQUIRED_MODELS:
		assert model in models

def test_generations(cars_api : Cars):
	generations = list(cars_api.get_generations(brand='Saab', model='9-3').keys())
	for generation in REQUIRED_GENERATIONS:
		assert generation in generations

def test_empty_generations(cars_api : Cars):
	result = cars_api.get_generations(brand='Saab', model='90')
	assert result is not None
	assert len(result) == 0
