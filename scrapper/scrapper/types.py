# Typing library imports
from typing import Any, Union

# Import Aliases
from selenium.webdriver import Chrome as BrowserType

# Key imports
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebElement

# Type Aliases
NullableString = Union[str, None]

# Type vealidation decorators


class Param:
	"""
	class that represents signle param in function that is verified via @verify_types
	"""
	def __init__(self, param_name: str, param_value: Any):
		"""
		constructs Param

		:param param_name: name of passsed argument
		:type param_name: str
		:param param_value: value od passed argument
		:type param_value: Any
		"""
		self.name = param_name
		self.value = param_value

	def is_nullable(self, defaults: dict) -> bool:
		"""
		checks is given type can be nullable

		:param defaults: map with default arguments of analyzed function
		:type defaults: dict
		:return: true if given param can be null
		:rtype: bool
		"""
		return self.name in defaults and defaults[self.name] is None

	def valid_type(self, expected: type, defaults: dict = {}) -> bool:
		"""
		validates type basing on annotations and defaults

		:param expected: expected type
		:type expected: type
		:param defaults: map of default arguments, defaults to {}
		:type defaults: dict, optional
		:return: true if given value fullfills requirements
		:rtype: bool
		"""
		if self.value is None:
			return self.is_nullable(defaults)
		else:
			return isinstance(self.value, expected)


def not_empty(param: Param):
	"""
	validates is length of given param is greater than 0

	:param param: argument o verify
	:type param: Param
	"""
	assert len(param.value) > 0, f'Argument `{param.name}` cannot be empty'


def verify_types(**checks):
	"""
	verifies is passed arguments matches annotations and applies additional checks

	:param checks: map of param_names with additionall checks
	:type checks: Dict[str, Function]
	:example checks: param_name=validate_function
	"""
	def verify_types_foo(foo):
		def verify_types_impl(*args, **kwargs):
			additional_checks = checks if checks is not None else {}
			function_name = foo.__name__
			annotations = foo.__annotations__
			defaults = foo.__kwdefaults__
			given_arguments = kwargs

			for param_name, param_value in given_arguments.items():
				if not param_name in annotations:
					continue  # ignore function kwargs
				param = Param(param_name, param_value)
				expected_type = annotations[param_name]
				assert param.valid_type(expected_type, defaults),\
					f'invalid type in function `{function_name}` on `{param.name}` param. Expected type: `{expected_type.__name__}`, but `{param.type.__name__}` given. Value = {param_value}'
				if param.value is None or param.name not in additional_checks:
					continue
				param_checks = additional_checks[param.name]
				param_checks = param_checks if isinstance(param_checks, list) else [param_checks]
				for check in param_checks:
					check(param)

			return foo(*args, **kwargs)
		return verify_types_impl
	return verify_types_foo
