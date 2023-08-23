import abc
from typing import Any, Dict, List, Tuple

try:
    from notebook.base.handlers import IPythonHandler
    from notebook.utils import url_path_join as ujoin
except ImportError:
    from jupyter_server.base.handlers import JupyterHandler as IPythonHandler
    from jupyter_server.utils import url_path_join as ujoin

from traitlets.config import Application


class BaseApp(Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log = self.parent.log
        if self.parent.name == "jupyter-notebook":
            self.update_tornado_settings(dict(root_dir=self.parent.notebook_dir))
        else:
            self.update_tornado_settings(dict(root_dir=self.parent.root_dir))

    @property
    def webapp(self):
        return self.parent.web_app

    def add_handlers(self, handlers: List[Tuple[str, IPythonHandler]]):
        """
        Add handlers to the tornado server

        Args:
            handlers -- a list of handlers
        """

        def rewrite(x):
            pat = ujoin(self.webapp.settings["base_url"], x[0].lstrip("/"))
            return (pat,) + x[1:]

        self.webapp.add_handlers(".*$", [rewrite(x) for x in handlers])

    def update_tornado_settings(self, settings: Dict[Any, Any]):
        """
        Update tornado settings

        Args:
            settings -- a settings dictionary used to update
                        the current tornado settings
        """
        self.webapp.settings.update(settings)

    def add_template_path(self, path: str):
        """
        Add a template path to the jinja environment

        Args:
                path -- the absolute path to the template directory
        """
        self.webapp.settings["e2xgrader"]["jinja_env"].loader.searchpath.append(path)

    @abc.abstractmethod
    def load_app(self):
        """
        This method is called when the app is loaded.
        Use it to initialize your app with handlers, settings, etc.
        """
        pass
