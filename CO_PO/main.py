import gc
from flask import Flask, render_template, request, redirect
import logging
from werkzeug.utils import secure_filename
from CO_PO.misc import close_main_thread_in_good_way, \
    save_path, get_paths, gen_template, auto_update
from CO_PO.matlab_related import Engine
from CO_PO import __version__

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)

WAITRESS = logging.getLogger("waitress")
WAITRESS.setLevel(logging.DEBUG)

app = Flask("CO-PO Mapping", template_folder=str(get_paths() / "templates"), static_folder=str(get_paths() / "static"))
logging.debug("Setting Template and static paths")


class Server(Engine):
    def __init__(self, port):
        super().__init__()
        self.port = port

    def get_status(self):
        template = gen_template(passed=True, force_refresh=False, ask_refresh=True)

        if not self.matlab_engine or self.is_engine_loading():
            template["status"] = "Matlab Engine is loading, Please wait until it loads..."
            template["force_refresh"] = True

        if not template["status"] and self.is_engine_busy():
            template["ask_refresh"] = True
            template["status"] = "Matlab Engine is busy, Please wait until it finishes...\nelse, You can use the " \
                                 "tools present at top right corner of the header "

        if not template["status"]:
            template["status"] = "Matlab Engine is running in the background.\nYou can request for any work."
            template["ask_refresh"] = False

        # Rare cases for this request to have passed as False

        template["passed"] = True
        return template

    def main_route(self):
        cell = self.get_status()

        logging.info(cell)

        if cell["force_refresh"]:
            return render_template(
                "/loading.html",
                title="Loading MatLab Engine",
                message=cell["status"],
                ask="/start-engine",
                estimated="(.5-3) min",
                show_image=False,
                auto_update=auto_update,
                version=__version__
            )

        return render_template(
            "index.html",
            from_stdout="1" if self.passed else "0",
            results=self.pure(),
            is_busy="1" if cell["ask_refresh"] else "",
            auto_update=auto_update,
            version=__version__
        )

    def start_engine(self):
        template = gen_template(
            message="Matlab Engine was already started, Refresh the Page once...", force_refresh=True
        )
        try:
            loaded = super().start_engine()
            template["passed"] = True

        except Exception as error:
            template["message"] = "Failed to load the Matlab Engine\n" + str(error)
            template["passed"] = False
            return template

        if loaded:
            return template

        while self.is_engine_loading():
            ...

        return template

    def close_session(self):
        self.stop_engine()
        del self.matlab_engine
        gc.collect()

        close_main_thread_in_good_way(1.3)
        return "You can close this session"

    def submit_input(self):
        response = self.get_status()
        logging.info("Submitted Input")

        response["passed"] = not (response["ask_refresh"] or response["force_refresh"])

        if not response["passed"]:
            response["status"] = "Failed to take your Input, as the server is already processing your another " \
                                 "request.\nPlease wait until your requests gets processed or use the tools at the " \
                                 "top right corner "
            return response

        file = request.files.get("raw", "")
        status, piece = tuple(save_path(secure_filename(file.filename)))
        response["passed"] = status

        if not status:
            response["status"] = piece
            return response

        file.save(piece)
        response.update(self.process(piece, request.form["exams"]))
        return response

    def force_restart(self):
        self.stop_engine()
        return redirect("/")

    def wait_for_processing(self):
        while self.is_engine_busy():
            ...
        return "1"


@app.route("/auto-updates", methods=["GET"])
def auto():
    asked = bool(int(request.args.get("auto-update", "0")))
    logging.info("Asked to turn auto-update to %s", "on" if asked else "off")
    auto_update(auto_update=asked)
    return gen_template(True, "changed")


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404
