from threading import Lock, Semaphore, current_thread
from typing import Dict, Union

from scrapper.server import WORKERS
from scrapper.types import verify_types

from scrapper.server.backend import BrowserInstance

class PoolSingleton:
	"""
	Carries handles for opened browsers
	"""

	MAX = WORKERS
	__instances : Dict[int, BrowserInstance] = dict()
	__instance_lock = Semaphore(MAX)
	__write_lock = Lock()

	def __init__(self, write : bool = False):
		if write:
			self.count = PoolSingleton.MAX
			PoolSingleton.__write_lock.acquire(blocking=True)
		else:
			self.count = 1

	def __enter__(self) -> "PoolSingleton":
		for _ in range(self.count):
			PoolSingleton.__instance_lock.acquire(blocking=True)
		return self

	def __exit__(self, *args, **kwargs):
		PoolSingleton.__instance_lock.release(self.count)
		if self.count == PoolSingleton.MAX:
			PoolSingleton.__write_lock.release()

	def add(self, id : int ) -> BrowserInstance:
		PoolSingleton.__instances[id] = BrowserInstance()
		return self.get(id)

	def get(self, id : int) -> Union[BrowserInstance, None]:
		return PoolSingleton.__instances.get(id)

	def quit(self) -> None:
		for _, browser in PoolSingleton.__instances.items():
			browser.finish()
		return PoolSingleton.__instances.clear() # return None

@verify_types()
def get_backend(*, quit : bool = False) -> Union[BrowserInstance, None]:
	if quit == True:
		with PoolSingleton(write=True) as ps:
			return ps.quit()

	# check is current thread is registered
	thread_id = current_thread().native_id
	with PoolSingleton() as ps:
		if ps.get(thread_id) is not None:
			return ps.get(thread_id)

	# if not returned, add missing browser, for current thread
	with PoolSingleton(write=True) as ps:
		return ps.add(thread_id)
