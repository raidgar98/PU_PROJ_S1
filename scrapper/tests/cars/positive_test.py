from tests.utils import Cars

REQUIRED_BRANDS = ['Audi', 'BMW', 'Opel', 'Ford', 'Syrena', 'Toyota', 'Alpine', 'Aro']
REQUIRED_MODELS = ["101", "102", "103", "104", "105", "Bosto", "Inny", "R-20"]
REQUIRED_GENERATIONS = ["I (1998-2002)","II (2003-2011)"]

TESTED_BRAND = 'Audi'
TESTED_MODEL = 'A4'
TESTED_GENERATION = 'B8 (2007-2015) (1246)'

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

def test_car_offer(cars_api : Cars):
	result = cars_api.list(brand=TESTED_BRAND, model=TESTED_MODEL, generation=TESTED_GENERATION, price_to=9999999)
	assert isinstance(result['max_page_num'], int)
	assert isinstance(result['urls'], list)
	assert result['max_page_num'] > 0

def test_car_offer_listing(cars_api : Cars):
	result_0 = cars_api.list(brand=TESTED_BRAND, model=TESTED_MODEL, generation=TESTED_GENERATION, page=1, price_to=9999999)
	result_1 = cars_api.list(brand=TESTED_BRAND, model=TESTED_MODEL, generation=TESTED_GENERATION, page=2, price_to=9999999)
	assert result_0['max_page_num'] == result_1['max_page_num']
	assert result_0['urls'][0] != result_1['urls'][0]
