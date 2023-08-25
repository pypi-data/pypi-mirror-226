from grader_labextension.api_handler import setup_handlers


def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "grader-labextension"
    }]


def _jupyter_server_extension_points():
    return [{
        "module": "grader_labextension"
    }]


def _load_jupyter_server_extension(server_app):
    """Register API handlers to receive HTTP requests from frontend extension.

    Parameters
    ----------
    server_app: jupyterlab.labapp.LabApp
        JupyterLab application instance
    """
    setup_handlers(server_app.web_app)
    name = "grader_labextension"
    server_app.log.info(f"Registered {name} server extension")


# For backward compatibility with notebook server, useful for Binder/JupyterHub
load_jupyter_server_extension = _load_jupyter_server_extension
