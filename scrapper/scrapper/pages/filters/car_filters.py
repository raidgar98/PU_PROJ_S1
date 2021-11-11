from scrapper.types import BrowserType, not_empty, verify_types

@verify_types(car_brand=not_empty, car_model=not_empty)
def setup_car_filters_impl(*, driver : BrowserType, car_brand : str, car_model : str, car_generation : str = None, **url_params) -> None:
