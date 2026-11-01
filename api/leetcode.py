# -*- coding: utf-8 -*-
"""
LeetCode API 封装（支持 leetcode.cn 与 leetcode.com，具备智能重试与异常容错能力）
"""
import json
from typing import Dict, Any, Optional

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

import urllib.request
import urllib.error


class LeetCodeAPI:
    """LeetCode GraphQL API 客户端"""

    def __init__(self, site: str = "cn", cookie: Optional[str] = None):
        """
        :param site: 'cn' 为力扣中国站 (leetcode.cn)，'com' 为全球站 (leetcode.com)
        :param cookie: 浏览器端 Cookie（针对中国站绕过 WAF 防爬盾时可选传入）
        """
        self.site = site.lower()
        if self.site == "cn":
            self.base_url = "https://leetcode.cn/graphql"
            self.referer = "https://leetcode.cn"
        else:
            self.base_url = "https://leetcode.com/graphql"
            self.referer = "https://leetcode.com"

        self.cookie = cookie
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": self.referer,
            "Origin": self.referer
        }
        if self.cookie:
            self.headers["Cookie"] = self.cookie

    def _post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """统一发送 POST 请求，优先使用 httpx，失败时回退至 urllib"""
        # 1. 优先使用 httpx
        if HAS_HTTPX:
            try:
                with httpx.Client(timeout=10.0, headers=self.headers, verify=False, follow_redirects=True) as client:
                    resp = client.post(self.base_url, json=payload)
                    if resp.status_code == 200:
                        text = resp.text.strip()
                        if text.startswith("{"):
                            return resp.json()
                        elif "alicfw" in text:
                            raise RuntimeError(
                                "力扣中国站触发了阿里云 WAF 防爬盾验证。\n"
                                "【解决方案】：\n"
                                "1. 浏览器打开 leetcode.cn 登录，F12 复制 Cookie 传入参数 --cookie '...'\n"
                                "2. 或者指定 --site com 查询全球站账号"
                            )
            except Exception as e:
                if "WAF" in str(e):
                    raise e

        # 2. 回退使用 urllib
        data_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(self.base_url, data=data_bytes, headers=self.headers, method="POST")
        try:
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=12, context=ctx) as resp:
                body = resp.read().decode("utf-8").strip()
                if body.startswith("{"):
                    return json.loads(body)
                elif "alicfw" in body:
                    raise RuntimeError("力扣中国站触发了 WAF 防爬盾验证，请使用 --cookie 传入浏览器 Cookie")
                else:
                    raise RuntimeError(f"返回非 JSON 响应: {body[:150]}")
        except Exception as e:
            raise RuntimeError(f"请求 LeetCode API 出错: {e}")

    def get_user_profile(self, username: str) -> Dict[str, Any]:
        """获取用户基本信息"""
        if self.site == "cn":
            query = """
            query userPublicProfile($username: String!) {
                userProfilePublicProfile(username: $username) {
                    username
                    profile {
                        realName
                        ranking
                    }
                    submissionProgress {
                        totalSubmissions
                        waSubmissions
                        acSubmissions
                        reSubmissions
                    }
                }
            }
            """
            return self._post({"query": query, "variables": {"username": username}})
        else:
            # leetcode.com 全球站查询
            query = """
            query getUserProfile($username: String!) {
                matchedUser(username: $username) {
                    username
                    profile {
                        realName
                        ranking
                    }
                    submitStatsGlobal {
                        acSubmissionNum {
                            difficulty
                            count
                        }
                    }
                }
            }
            """
            res = self._post({"query": query, "variables": {"username": username}})
            # 适配成统一的返回结构
            matched = res.get("data", {}).get("matchedUser") or {}
            profile_info = matched.get("profile") or {}
            ac_list = (matched.get("submitStatsGlobal") or {}).get("acSubmissionNum") or []
            total_ac = 0
            for item in ac_list:
                if item.get("difficulty") == "All":
                    total_ac = item.get("count", 0)

            return {
                "data": {
                    "userProfilePublicProfile": {
                        "username": matched.get("username", username),
                        "profile": profile_info,
                        "submissionProgress": {
                            "totalSubmissions": total_ac * 2,  # 估算提交
                            "acSubmissions": total_ac
                        }
                    }
                }
            }

    def get_submission_stats(self, username: str) -> Dict[str, Any]:
        """获取题目提交统计"""
        if self.site == "cn":
            query = """
            query userProfileQuestions($username: String!) {
                allQuestionsCount {
                    difficulty
                    count
                }
                matchedUser(username: $username) {
                    submitStats {
                        acSubmissionNum {
                            difficulty
                            count
                        }
                    }
                }
            }
            """
            return self._post({"query": query, "variables": {"username": username}})
        else:
            # leetcode.com 全球站
            query = """
            query getUserStats($username: String!) {
                allQuestionsCount {
                    difficulty
                    count
                }
                matchedUser(username: $username) {
                    submitStatsGlobal {
                        acSubmissionNum {
                            difficulty
                            count
                        }
                    }
                }
            }
            """
            res = self._post({"query": query, "variables": {"username": username}})
            matched = res.get("data", {}).get("matchedUser") or {}
            submit_stats = matched.get("submitStatsGlobal") or {}
            return {
                "data": {
                    "allQuestionsCount": res.get("data", {}).get("allQuestionsCount", []),
                    "matchedUser": {
                        "submitStats": submit_stats
                    }
                }
            }
