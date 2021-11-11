# Typing library imports
from typing import Any, Union, _SpecialForm

# Key imports
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebElement

# Import Aliases
from selenium.webdriver import Chrome as BrowserType

# Type Aliases
NullableString = Union[str, None]

# Type vealidation decorators
class Param:
	def __init__(self, param_name : str, param_value : Any):
		self.name = param_name
		self.value = param_value

	def is_nullable(self, defaults : dict) -> bool:
		return self.name in defaults and defaults[self.name] is None

	def valid_type(self, expected : type, defaults : dict = {}) -> bool:
		if self.value is None:
			return self.is_nullable(defaults)
		else:
			return isinstance(self.value, expected)

def not_empty(param : Param):
	assert len(param.value) > 0, f'Argument `{param.name}` cannot be empty'

def verify_types(**checks):
	def verify_types_foo(foo):
		def verify_types_impl(**kwargs):
			additional_checks = checks if checks is not None else {}
			function_name = foo.__name__
			annotations = foo.__annotations__
			defaults = foo.__kwdefaults__
			given_arguments = kwargs

			for param_name, param_value in given_arguments.items():
				if not param_name in annotations: continue # ignore function kwargs
				param = Param(param_name, param_value)
				expected_type = annotations[param_name]
				assert param.valid_type(expected_type, defaults),\
					f'invalid type in function `{function_name}` on `{param.name}` param. Expected type: `{expected_type.__name__}`, but `{param.type.__name__}` given. Value = {param_value}'
				if param.value is None or param.name not in additional_checks : continue
				param_checks = additional_checks[param.name]
				param_checks = param_checks if isinstance(param_checks, list) else [param_checks]
				for check in param_checks:
					check(param)

			return foo(**kwargs)
		return verify_types_impl
	return verify_types_foo
