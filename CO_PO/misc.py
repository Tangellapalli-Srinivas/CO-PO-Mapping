import socket
import subprocess
import webbrowser
from threading import Timer
from _thread import interrupt_main
import pathlib
import tempfile
import os
import json
import logging


def close_main_thread_in_good_way(wait=0.9):
    logging.warning("Shutting down....")
    return Timer(wait, lambda: interrupt_main()).start()


def open_local_url(port_, wait=1, postfix=""):
    logging.info("Requested to open %s", f"http://localhost:{port_}/" + postfix)
    return Timer(wait, lambda: webbrowser.open(f"http://localhost:{port_}/" + postfix)).start()


def get_free_port():
    logging.info("Getting a free port")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("localhost", 0))
        port_ = sock.getsockname()[1]
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return port_


def save_path(path):
    logging.info("Requested to save %s to temp directory", path)

    if not path:
        yield False
        yield "File was not properly uploaded"
        return

    focus = pathlib.Path(path)
    root = pathlib.Path(__file__).parent / "temp"
    root.mkdir(exist_ok=True)
    passed = focus.suffix == ".xlsx"

    if not passed:
        yield passed
        yield "Invalid Extension, Make sure to upload only excel files (*.xlsx, *.xls)"
        return

    if focus.name.startswith("~$"):
        yield False
        yield "Excel files whose name starting with '~$' are not considered, Please rename the file."
        return

    yield True
    handle, path = tempfile.mkstemp(suffix=focus.suffix, dir=root)
    os.close(handle)
    yield pathlib.Path(path)


def get_paths():
    return pathlib.Path(__file__).parent


def gen_template(passed=False, status="", **kwargs):
    kwargs["passed"] = passed
    kwargs["status"] = status
    return kwargs


def auto_update(get=False, **kwargs):
    settings = pathlib.Path(__file__).parent / "settings.json"
    ... if settings.exists() else settings.write_text("{}")

    temp = json.loads(settings.read_text())
    if get:
        return temp

    temp.update(kwargs)

    settings.write_text(json.dumps(temp))
    return temp


def ask_for_update():
    ask = auto_update(True).get("auto_update", False)
    if not ask:
        return

    logging.info("asking for the update...")
    return subprocess.Popen(
        ["powershell.exe", "-file", str(pathlib.Path(__file__).parent.parent / "gate.ps1"), "-mode 2"]
    )
