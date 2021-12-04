from pathlib import Path
from signal import SIGKILL
from subprocess import Popen

from pytest import yield_fixture


@yield_fixture(scope='session')
def api() -> str:
	path = Path(__file__).parent.parent.resolve()
	proc = Popen(['python3', path.joinpath('main.py')])
	yield 'http://localhost:8090'
	proc.send_signal(SIGKILL)
	assert proc.wait(1.0) == 0
