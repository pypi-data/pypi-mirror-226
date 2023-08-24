from .handlers import RouteHandler
from jupyter_server.extension.application import ExtensionApp
from traitlets import List

class ETCJupyterLabTelemetryProducerDemoApp(ExtensionApp):

    name = "etc_jupyterlab_telemetry_producer_demo"

    activeEvents = List([]).tag(config=True)
    logNotebookContentEvents = List([]).tag(config=True)

    def initialize_settings(self):
        try:
            # assert self.activeEvents, "The c.ETCJupyterLabTelemetryProducerDemoApp.activeEvents configuration setting must be set."
            pass

        except Exception as e:
            self.log.error(str(e))
            raise e

    def initialize_handlers(self):
        try:
            self.handlers.extend([(r"/etc_jupyterlab_telemetry_producer_demo/(.*)", RouteHandler)])
        except Exception as e:
            self.log.error(str(e))
            raise e