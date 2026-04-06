'''mihomo_manager - AstrBot 插件'''
from astrbot.api import logger
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.core import AstrBotConfig

@register("mihomo_manager", "jyjyjyjjyyl & AI", "mihomo 仓库自动化管理插件", "1.0.0")
class MihomoManager(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.repo_owner = config.get("repo_owner", "Kess66666")
        self.repo_name = config.get("repo_name", "mihomo")
        logger.info(f"[mihomo_manager] 插件已加载")

    @filter.command("mihomo", alias={"mh"})
    async def mihomo_help(self, event: AstrMessageEvent):
        yield event.plain_result("🔧 mihomo_manager 插件就绪")

    async def terminate(self):
        logger.info("[mihomo_manager] 插件已卸载")