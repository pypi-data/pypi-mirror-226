from typing import Optional
from collections.abc import Callable
import uuid
from navconfig.logging import logging
from navigator.types import WebApp
from navigator.applications.base import BaseApplication
from abc import ABCMeta, abstractmethod


class TriggerResponse:
    pass

class BaseTrigger(metaclass=ABCMeta):
    # Signal for startup method for this ModelView
    on_startup: Optional[Callable] = None

    """BaseTrigger.

        Base class for all Triggers in FlowTask.
    """
    def __init__(self, description: str, *args, **kwargs):
        self.trigger_id = uuid.uuid4()
        self.description = description
        self.response = None
        self._args = args
        self._kwargs = kwargs
        self.app: WebApp = None
        self.logger = logging.getLogger(f"Trigger.{self.__class__.__name__}")

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
        # startup operations over extension backend
        if callable(self.on_startup):
            app.on_startup.append(self.on_startup)
