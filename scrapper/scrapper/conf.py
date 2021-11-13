from sys import stdout as STDOUT
from logging import DEBUG, INFO, Formatter, Logger, StreamHandler, getLogger


def get_logger() -> Logger:
	logger = getLogger('PU_SEM_1')
	logger.handlers.clear()

	stream_handler = StreamHandler(STDOUT)
	stream_handler.setFormatter(Formatter("[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] %(message)s"))
	logger.addHandler(stream_handler)
	logger.setLevel(INFO)
	return logger


BASE_URL = 'https://www.otomoto.pl'
WORKERS = 10
