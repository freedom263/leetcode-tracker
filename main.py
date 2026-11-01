#!/usr/bin/env python3
"""
LeetCode Tracker - 命令行工具
"""
import click
import sys
from api.leetcode import LeetCodeAPI
from analyzer.stats import StatsAnalyzer


@click.command()
@click.option('--username', '-u', required=True, help='LeetCode 用户名')
def main(username):
    """获取并分析 LeetCode 刷题数据"""
    try:
        api = LeetCodeAPI()
        analyzer = StatsAnalyzer()

        click.echo(f"正在获取用户 {username} 的数据...\n")

        profile_data = api.get_user_profile(username)
        analyzer.display_profile(profile_data)

        click.echo("\n正在分析题目完成情况...\n")
        stats_data = api.get_submission_stats(username)
        analyzer.display_difficulty_stats(stats_data)

    except Exception as e:
        click.echo(f"错误: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
