#!/usr/bin/python3

from scrapper.conf import WORKERS, get_logger, Logger
from scrapper.server.engine import run_server
from argparse import ArgumentParser
from sys import argv

log : Logger = get_logger()
engine = ArgumentParser()

engine.add_argument('-p', '--port', dest='port', type=int, default=8090, help='port which will be used for listening')
engine.add_argument('-j', '--jobs', dest='jobs', type=int, default=WORKERS, help='amount of threads to use while running')
engine.add_argument('-i', '--interface', dest='iface', type=str, default='0.0.0.0', help='interface to listen on')

parsed_args = engine.parse_args(list(argv[1:]))

try:
	run_server(port=parsed_args.port, interface=parsed_args.iface, workers=parsed_args.jobs)
except KeyboardInterrupt:
	log.info('stopped server on user request')
	exit_code = 0
except Exception as e:
	log.info('stopped server with unknown exception: ', e)
	exit_code = -1

exit(exit_code)
