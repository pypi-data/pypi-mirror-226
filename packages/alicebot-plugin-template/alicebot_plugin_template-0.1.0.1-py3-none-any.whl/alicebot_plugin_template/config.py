"""插件配置。"""

from alicebot import ConfigModel


class Config(ConfigModel):
    """插件配置。

    Attributes:
        greet_message: 欢迎信息。
    """

    __config_name__ = "hello_plugin"

    greet_message: str = "Hello, I'm Alice!"
