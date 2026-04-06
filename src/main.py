'''mihomo_manager - AstrBot 插件'''
from astrbot.api import logger
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.core import AstrBotConfig
import asyncio
import aiohttp
import json
from datetime import datetime

@register("mihomo_manager", "jyjyjyjjyyl & AI Assistant", "管理 mihomo 仓库的 GitHub Actions 自动构建、定时同步和 Docker 状态检查", "1.0.0")
class MihomoManager(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.repo_owner = config.get("repo_owner", "Kess66666")
        self.repo_name = config.get("repo_name", "mihomo")
        self.main_workflow = config.get("main_workflow", "fully-compatible-build.yml")
        self.github_token = config.get("github_token", "")
        
    async def initialize(self):
        '''插件初始化'''
        logger.info(f"mihomo_manager 插件已初始化，仓库: {self.repo_owner}/{self.repo_name}")
        
    @filter.command("mihomo_status")
    async def mihomo_status(self, event: AstrMessageEvent):
        '''查看 mihomo 仓库状态和最近构建'''
        try:
            # 获取最近工作流运行
            runs_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/runs"
            headers = {"Authorization": f"token {self.github_token}"} if self.github_token else {}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(runs_url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        runs = data.get("workflow_runs", [])[:3]  # 最近3次运行
                        
                        if runs:
                            result = f"🔍 **{self.repo_owner}/{self.repo_name}** 最近构建状态:\n\n"
                            for run in runs:
                                status_emoji = "✅" if run["conclusion"] == "success" else "❌" if run["conclusion"] == "failure" else "🔄"
                                created_at = datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))
                                result += f"{status_emoji} **{run['name']}**\n"
                                result += f"   状态: {run['status']} | 结论: {run['conclusion']}\n"
                                result += f"   触发: {run['event']} | 时间: {created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
                        else:
                            result = f"📭 没有找到 {self.repo_owner}/{self.repo_name} 的工作流运行记录"
                    else:
                        result = f"❌ 获取工作流状态失败: HTTP {resp.status}"
                        
            yield event.plain_result(result)
        except Exception as e:
            logger.error(f"获取 mihomo 状态失败: {e}")
            yield event.plain_result(f"❌ 获取状态失败: {str(e)}")
            
    @filter.command("mihomo_trigger")
    async def mihomo_trigger(self, event: AstrMessageEvent):
        '''手动触发 mihomo 构建工作流'''
        if not self.github_token:
            yield event.plain_result("❌ 未配置 GitHub Token，无法触发工作流")
            return
            
        try:
            # 触发工作流
            trigger_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/workflows/{self.main_workflow}/dispatches"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            payload = {"ref": "main"}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(trigger_url, headers=headers, json=payload) as resp:
                    if resp.status == 204:
                        result = f"✅ 已触发 {self.main_workflow} 工作流\n\n"
                        result += "🔗 查看运行状态: https://github.com/{self.repo_owner}/{self.repo_name}/actions"
                    else:
                        result = f"❌ 触发工作流失败: HTTP {resp.status}"
                        
            yield event.plain_result(result)
        except Exception as e:
            logger.error(f"触发 mihomo 工作流失败: {e}")
            yield event.plain_result(f"❌ 触发工作流失败: {str(e)}")