# -*- coding: utf-8 -*-
"""
数据存储模块 - 支持将用户 LeetCode 刷题数据持久化到本地 JSON 文件
"""
import os
import json
from datetime import datetime
from typing import Dict, Any


class DataStorage:
    """本地数据存储管理器"""

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # 默认保存在当前 leetcode-tracker 项目根目录下的 data 文件夹
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.data_dir = os.path.join(base_dir, "data")
        else:
            self.data_dir = data_dir

        os.makedirs(self.data_dir, exist_ok=True)

    def save_user_data(self, username: str, profile_data: Dict[str, Any], stats_data: Dict[str, Any]) -> str:
        """保存用户的个人资料和题目统计数据到本地 JSON"""
        record = {
            "username": username,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "profile": profile_data,
            "stats": stats_data
        }

        file_path = os.path.join(self.data_dir, f"{username}_stats.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)

        return file_path

    def load_user_data(self, username: str) -> Dict[str, Any]:
        """读取本地保存的用户历史数据"""
        file_path = os.path.join(self.data_dir, f"{username}_stats.json")
        if not os.path.exists(file_path):
            return {}

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
