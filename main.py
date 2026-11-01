#!/usr/bin/env python3
"""
LeetCode Tracker - 命令行工具
"""
import click


@click.command()
@click.option('--username', '-u', required=True, help='LeetCode 用户名')
def main(username):
    """获取并分析 LeetCode 刷题数据"""
    click.echo(f"正在获取用户 {username} 的数据...")
    # TODO: 实现数据获取逻辑


if __name__ == '__main__':
    main()
