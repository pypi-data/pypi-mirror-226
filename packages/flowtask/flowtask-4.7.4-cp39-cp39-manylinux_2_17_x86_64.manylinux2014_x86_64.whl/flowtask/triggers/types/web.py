from aiohttp import web
from navigator.views import BaseHandler
from navigator.types import WebApp
from .base import BaseTrigger, TriggerResponse


class WebTrigger(BaseTrigger, BaseHandler):
    """WebTrigger.

        Can be used to receive data from a web URL.
    """
    def __init__(self, description: str, *args, **kwargs):
        BaseHandler.__init__(self, *args, **kwargs)
        BaseTrigger.__init__(self, description, *args, **kwargs)
        self.url = f"/api/v1/triggers/webhook/{self.trigger_id}"

    def setup(self, app: WebApp) -> None:
        super().setup(app)
        print('CALLING SETUP for WebHook Trigger')
        self.logger.notice(
            f"Set the unique URL Trigger to: {self.url}"
        )
        self.app.router.add_route('GET', self.url, self.get)
        self.app.router.add_route('POST', self.url, self.post)

    async def get(self, request: web.Request, *args, **kwargs):
        print('CALLING GET')
        headers = {
            "x-status": "Empty",
            "x-message": "Module information not found",
        }
        return self.no_content(headers=headers)

    async def post(self, request: web.Request, *args, **kwargs):
        pass
