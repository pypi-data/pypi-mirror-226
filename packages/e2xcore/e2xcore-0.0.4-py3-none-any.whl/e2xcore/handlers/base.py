from nbgrader.server_extensions.formgrader.base import BaseApiHandler

try:
    from notebook.base.handlers import IPythonHandler
except ImportError:
    from jupyter_server.base.handlers import JupyterHandler as IPythonHandler

from ..api import E2xAPI


class E2xHandler(IPythonHandler):
    @property
    def e2xgrader_settings(self):
        return self.settings["e2xgrader"]

    @property
    def jinja_env(self):
        return self.e2xgrader_settings["jinja_env"]

    @property
    def menu(self):
        return self.e2xgrader_settings["menu"]

    def render(self, name, **ns):
        template = self.jinja_env.get_template(name)
        return template.render(**ns)


class E2xApiHandler(BaseApiHandler):
    @property
    def api(self):
        level = self.log.level
        api = E2xAPI(self.coursedir, self.authenticator, parent=self.coursedir.parent)
        api.log_level = level
        return api
