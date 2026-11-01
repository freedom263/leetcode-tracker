"""
LeetCode API 封装
"""
import httpx
from typing import Dict, Any


class LeetCodeAPI:
    """LeetCode GraphQL API 客户端"""

    def __init__(self):
        self.base_url = "https://leetcode.cn/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

    def get_user_profile(self, username: str) -> Dict[str, Any]:
        """获取用户基本信息"""
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

        variables = {"username": username}
        response = requests.post(
            self.base_url,
            json={"query": query, "variables": variables},
            headers=self.headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def get_submission_stats(self, username: str) -> Dict[str, Any]:
        """获取题目提交统计"""
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

        variables = {"username": username}
        response = requests.post(
            self.base_url,
            json={"query": query, "variables": variables},
            headers=self.headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
