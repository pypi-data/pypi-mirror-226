from nonebot import get_driver

from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="{星崽Bot-菜单}",
    description="{为星崽系列插件提供菜单}",
    usage="{能力中心}",

    type="{application}",

    homepage="{https://github.com/StarJian-Team/StarZai-Bot/tree/main/Memu/NoneBot}",
    # 发布必填。

    config=Config,
    # 插件配置项类，如无需配置可不填写。

    supported_adapters={"~onebot.v11"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

global_config = get_driver().config
config = Config.parse_obj(global_config)


from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters.onebot.v11 import MessageSegment

memu = on_command("能力中心", rule=to_me(), aliases={"memu"}, priority=10, block=True)

@memu.handle()
async def handle_picture():
    # 构造图片消息段
    image = MessageSegment.image("https://v2.nonebot.dev/logo.png")
    # 发送图片
    await memu.send(image)