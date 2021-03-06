"""
:source: https://stackoverflow.com/a/25580545/11738218
"""

from json import dumps
from os.path import join as join_path
from urllib.parse import ParseResult, parse_qsl, unquote, urlencode, urlparse


def update_url(url, *, path: list = [], **params):
	""" Add path and GET params to provided URL being aware of existing.

	:param url: string of target URL
	:param params: dict containing requested params to be added
	:return: string with updated URL
	"""
	# Unquoting URL first so we don't loose existing args
	url = unquote(url)
	# Extracting url info
	parsed_url = urlparse(url)
	# Extracting URL arguments from parsed URL
	get_args = parsed_url.query
	get_path = parsed_url.path
	# Converting URL arguments to dict
	parsed_get_args = dict(parse_qsl(get_args))
	# Merging URL arguments dict with new params
	parsed_get_args.update(params)

	# Bool and Dict values should be converted to json-friendly values
	# you may throw this part away if you don't like it :)
	parsed_get_args.update(
		{k: dumps(v) for k, v in parsed_get_args.items()
			if isinstance(v, (bool, dict))}
	)

	# Converting URL argument to proper query string
	encoded_get_args = urlencode(parsed_get_args, doseq=True)

	# Extending path
	for path_part in path:
		get_path = join_path(get_path, path_part)

	# Creating new parsed result object based on provided with new
	# URL arguments. Same thing happens inside of urlparse.
	new_url = ParseResult(
		parsed_url.scheme, parsed_url.netloc, get_path,
		parsed_url.params, encoded_get_args, parsed_url.fragment
	).geturl()

	return new_url
