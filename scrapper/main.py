#!/usr/bin/python3

from scrapper.conf import get_logger, Logger
from scrapper.server.engine import run_server

log : Logger = get_logger()

try:
	run_server(port=8090)
except KeyboardInterrupt:
	log.info('stopped server on user request')
	exit_code = 0
except Exception as e:
	log.info('stopped server with unknown exception: ', e)
	exit_code = -1

exit(exit_code)
