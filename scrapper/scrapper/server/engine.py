import socketserver as SocketServer
import typing

from concurrent.futures import ThreadPoolExecutor
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from threading import current_thread

from jsonrpcserver import dispatch
from scrapper.server import WORKERS
from scrapper.server.browser_pool import get_backend
from scrapper.server.endpoints import build_methods


def log_thread_id(alias : str):
	print(f'{alias} current thread id: {current_thread().native_id}', flush=True)

class PoolManager(ThreadingMixIn):
	pool = ThreadPoolExecutor(max_workers=WORKERS, initializer=lambda : print(f'creating new browser: {get_backend()}'))
	def process_request(self, request, client_address) -> None:
		log_thread_id('process_request')
		PoolManager.pool.submit(self.process_request_thread, request, client_address)

class PoolHTTPServer(PoolManager, HTTPServer): pass
class Handler(BaseHTTPRequestHandler):
	def __init__(self, methods, *args, **kwargs):
		self.methods = methods
		super().__init__(*args, **kwargs)

	def do_POST(self):
		request = self.rfile.read(int(self.headers["Content-Length"])).decode()
		response = dispatch(request, methods=self.methods, context=get_backend())
		self.send_response(200)
		self.end_headers()
		self.wfile.write(response.encode('utf-8'))


def run_server(port):
	try:
		server = PoolHTTPServer(('', port), partial(Handler, build_methods()))
		server.serve_forever()
	finally:
		get_backend(quit=True)

