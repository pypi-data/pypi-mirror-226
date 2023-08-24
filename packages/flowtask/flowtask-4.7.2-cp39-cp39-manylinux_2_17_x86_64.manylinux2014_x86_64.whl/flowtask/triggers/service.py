import asyncio
from navigator.types import WebApp
from navigator.applications.base import BaseApplication
from .types.base import BaseTrigger

class TriggerService:
    def __init__(self, event_loop: asyncio.AbstractEventLoop):
        self._loop = event_loop
        self._triggers: list = []
        self._started: bool = False
        self.app: WebApp = None

    def add_trigger(self, trigger: BaseTrigger):
        self._triggers.append(trigger)
        trigger.setup(app=self.app)

    def setup(self, app: WebApp) -> None:
        """setup.

            Configuration of Trigger when started.
        Args:
            app (aiohttp.web.Application): Web Application.
        """
        if isinstance(app, BaseApplication):  # migrate to BaseApplication (on types)
            self.app = app.get_app()
        elif isinstance(app, WebApp):
            self.app = app  # register the app into the Extension
        else:
            raise TypeError(
                f"Invalid type for Application Setup: {app}:{type(app)}"
            )
        # mark service as started.
        self._started = True
