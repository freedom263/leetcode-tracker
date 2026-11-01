# -*- coding: utf-8 -*-
"""
LeetCode Tracker - 命令行工具
"""
import sys
import os

# 适配 Windows GBK 终端编码
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import click
from api.leetcode import LeetCodeAPI
from analyzer.stats import StatsAnalyzer
from utils.storage import DataStorage


@click.command()
@click.option('--username', '-u', required=True, help='LeetCode 用户名')
@click.option('--site', '-s', default='com', type=click.Choice(['cn', 'com']), help='站点选择: cn (力扣中国站) 或 com (全球站，推荐默认)')
@click.option('--cookie', '-c', default=None, help='力扣中国站 Cookie（可选，用于绕过 WAF 防爬盾）')
@click.option('--save/--no-save', default=True, help='是否将数据自动保存至本地 JSON（默认开启）')
def main(username, site, cookie, save):
    """获取并分析 LeetCode 刷题数据与进度量化"""
    analyzer = StatsAnalyzer()
    storage = DataStorage()
    try:
        api = LeetCodeAPI(site=site, cookie=cookie)

        analyzer.console.print(f"\n[cyan]正在获取 [{site.upper()}站] 用户 {username} 的刷题数据...[/cyan]\n")

        profile_data = api.get_user_profile(username)
        analyzer.display_profile(profile_data)

        analyzer.console.print("\n[cyan]正在分析题目完成情况...[/cyan]\n")
        stats_data = api.get_submission_stats(username)
        analyzer.display_difficulty_stats(stats_data)

        # 本地数据持久化
        if save:
            saved_file = storage.save_user_data(username, profile_data, stats_data)
            analyzer.console.print(f"\n[green]数据已自动持久化保存至: {saved_file}[/green]\n")

    except Exception as e:
        analyzer.console.print(f"\n[red]错误: {str(e)}[/red]\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
