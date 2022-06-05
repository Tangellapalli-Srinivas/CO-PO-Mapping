import urllib.error
from typing import Union, List
from CO_PO import __version__
from CO_PO.misc import get_free_port, open_local_url, auto_update
from CO_PO.main import Server, app
from waitress import serve
from urllib.request import urlopen
import json
import subprocess
import pathlib


def get_version():
    with urlopen("https://api.github.com/repos/Tangellapalli-Srinivas/CO-PO-Mapping/releases/latest") as response:
        parsed = json.loads(response.read())
        return parsed["tag_name"]


def call_shell(mode, get_args=False) -> Union[subprocess.Popen, List]:
    args = ["powershell.exe", "-file", str(pathlib.Path(__file__).parent.parent / "gate.ps1"), "-mode", str(mode)]
    if get_args:
        return args
    return subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_CONSOLE, close_fds=True)


def call_shell_wait(message):
    args = call_shell(4, get_args=True)
    args.append("-arguments")
    args.append(message)
    return subprocess.run(args, close_fds=True)


def compare_version():
    return __version__ != get_version()


stop = True
try:
    assert get_version().startswith("v0.0")
    stop = False
except AssertionError as error:
    call_shell_wait("Trial Version Expired!, Uninstalling Files...")
    call_shell(3)
except urllib.error.HTTPError as _:
    call_shell_wait(str(_.reason) + "\nPlease check your internet connection.")
except urllib.error.URLError as _:
    call_shell_wait(str(_.reason) + "\nPlease check your internet connection.")
except Exception as _:
    call_shell_wait(str(_))

if stop:
    exit(0)

if __name__ == "__main__":
    server = Server(get_free_port())

    open_local_url(server.port)

    app.add_url_rule("/", view_func=server.main_route)

    app.add_url_rule("/close-session", view_func=server.close_session)
    app.add_url_rule("/submit-input", view_func=server.submit_input, methods=["POST"])
    app.add_url_rule("/get-status", view_func=server.get_status)
    app.add_url_rule("/restart", view_func=server.force_restart)
    app.add_url_rule("/start-engine", view_func=server.start_engine)
    app.add_url_rule("/wait-for-processing", view_func=server.wait_for_processing)

    serve(app, port=server.port)

    call_shell(2) if auto_update(True).get("auto_update", False) and compare_version() else ...
