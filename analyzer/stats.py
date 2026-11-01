"""
数据分析模块
"""
from typing import Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class StatsAnalyzer:
    """统计数据分析器"""

    def __init__(self):
        self.console = Console()

    def display_profile(self, profile_data: Dict[str, Any]):
        """显示用户基本信息"""
        user_data = profile_data.get("data", {}).get("userProfilePublicProfile", {})

        if not user_data:
            self.console.print("[red]用户不存在或数据获取失败[/red]")
            return

        username = user_data.get("username", "N/A")
        ranking = user_data.get("profile", {}).get("ranking", "N/A")

        progress = user_data.get("submissionProgress", {})
        total = progress.get("totalSubmissions", 0)
        ac = progress.get("acSubmissions", 0)

        pass_rate = f"{(ac / total * 100):.1f}%" if total > 0 else "0.0%"
        info_text = f"""
用户名: {username}
全站排名: {ranking}
总提交数: {total}
通过提交数: {ac}
通过率: {pass_rate}
        """.strip()

        self.console.print(Panel(info_text, title="[bold blue]用户信息[/bold blue]"))

    def display_difficulty_stats(self, stats_data: Dict[str, Any]):
        """显示难度分布统计"""
        data = stats_data.get("data", {})

        all_questions = {q["difficulty"]: q["count"]
                        for q in data.get("allQuestionsCount", [])}

        user_ac = data.get("matchedUser", {}).get("submitStats", {}).get("acSubmissionNum", [])
        user_ac_dict = {item["difficulty"]: item["count"] for item in user_ac}

        table = Table(title="题目完成情况")
        table.add_column("难度", style="cyan")
        table.add_column("已完成", style="green")
        table.add_column("总数", style="yellow")
        table.add_column("完成率", style="magenta")

        for difficulty in ["Easy", "Medium", "Hard"]:
            total = all_questions.get(difficulty, 0)
            completed = user_ac_dict.get(difficulty, 0)
            rate = f"{(completed/total*100):.1f}%" if total > 0 else "0%"

            table.add_row(
                difficulty,
                str(completed),
                str(total),
                rate
            )

        self.console.print(table)
