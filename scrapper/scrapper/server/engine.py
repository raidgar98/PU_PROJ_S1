import json
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

from jsonrpcserver import dispatch
from scrapper.conf import WORKERS, get_logger
from scrapper.server.browser_pool import get_backend
from scrapper.server.endpoints import build_methods

log = get_logger()


class PoolManager(ThreadingMixIn):
	pool = None

	def setup_pool(workers : int = WORKERS):
		PoolManager.pool = ThreadPoolExecutor(max_workers=workers, initializer=get_backend)

	def process_request(self, request, client_address) -> None:
		PoolManager.pool.submit(self.process_request_thread, request, client_address)


class PoolHTTPServer(PoolManager, HTTPServer):
	pass


class Handler(BaseHTTPRequestHandler):
	def __init__(self, methods, *args, **kwargs):
		self.methods = methods
		super().__init__(*args, **kwargs)

	def do_POST(self):
		request = self.rfile.read(int(self.headers["Content-Length"])).decode()
		response = Handler.perform_dispatch(request, self.methods)
		self.send_response(200)
		self.end_headers()
		self.wfile.write(response.encode('utf-8'))

	@classmethod
	def perform_dispatch(cls, request : str, methods : dict):
		return dispatch(request, methods=methods, context=get_backend(), serializer=partial(json.dumps, ensure_ascii=False, default=vars))


def run_server(*, port : int, interface : str = '0.0.0.0', workers : int = WORKERS):
	try:
		PoolManager.setup_pool(workers)
		server = PoolHTTPServer((interface, port), partial(Handler, build_methods()))
		log.info(f'serven listen on {interface}:{port}')
		server.serve_forever()
	finally:
		print(flush=True)
		log.info('stopping server, please be patient...')
		get_backend(quit=True)
