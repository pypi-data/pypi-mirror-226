from typing import Any

from alicebot import Plugin
from alicebot.event import MessageEvent

from .config import Config


class HelloPlugin(Plugin[MessageEvent[Any], None, Config], config=Config):
    async def handle(self) -> None:
        """处理事件。"""
        await self.event.reply(self.config.greet_message)

    async def rule(self) -> bool:
        """匹配事件。"""
        return (
            isinstance(self.event, MessageEvent)
            and self.event.get_plain_text() == "hello"
        )
