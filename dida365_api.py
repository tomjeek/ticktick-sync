#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
滴答清单 API 封装
基于官方文档：https://developer.dida365.com/

Author: memU Bot
Version: 2.0.0
Date: 2026-03-02
"""

import requests
from datetime import datetime
from typing import Optional, Dict, List, Any


class Dida365Client:
    """滴答清单 API 客户端"""

    def __init__(self, access_token: str, timezone: str = "Asia/Shanghai"):
        """
        初始化客户端

        Args:
            access_token: 滴答清单 Access Token
            timezone: 时区，默认 Asia/Shanghai
        """
        self.access_token = access_token
        self.timezone = timezone
        self.api_base = "https://api.dida365.com/open/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        发送 HTTP 请求

        Args:
            method: HTTP 方法
            endpoint: API 端点
            **kwargs: 额外参数

        Returns:
            响应 JSON 数据
        """
        url = f"{self.api_base}{endpoint}"
        response = self.session.request(method, url, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_projects(self) -> List[Dict[str, Any]]:
        """
        获取所有项目

        Returns:
            项目列表
        """
        return self._request("GET", "/project")

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """
        获取项目详情

        Args:
            project_id: 项目 ID

        Returns:
            项目详情
        """
        return self._request("GET", f"/project/{project_id}")

    def get_project_data(self, project_id: str) -> Dict[str, Any]:
        """
        获取项目和任务数据

        Args:
            project_id: 项目 ID

        Returns:
            项目和任务数据
        """
        return self._request("GET", f"/project/{project_id}/data")

    def create_project(self, name: str, color: str = "", is_group: bool = False) -> Dict[str, Any]:
        """
        创建项目

        Args:
            name: 项目名称
            color: 项目颜色
            is_group: 是否为项目组

        Returns:
            创建的项目
        """
        data = {
            "name": name,
            "color": color,
            "isGroup": is_group
        }
        return self._request("POST", "/project", json=data)

    def update_project(self, project_id: str, **kwargs) -> Dict[str, Any]:
        """
        更新项目

        Args:
            project_id: 项目 ID
            **kwargs: 更新的字段

        Returns:
            更新后的项目
        """
        return self._request("POST", f"/project/{project_id}", json=kwargs)

    def delete_project(self, project_id: str) -> Dict[str, Any]:
        """
        删除项目

        Args:
            project_id: 项目 ID

        Returns:
            删除结果
        """
        return self._request("DELETE", f"/project/{project_id}")

    def create_task(
        self,
        title: str,
        project_id: str,
        content: str = "",
        due_date: Optional[str] = None,
        priority: int = 0,
        is_all_day: bool = False
    ) -> Dict[str, Any]:
        """
        创建任务

        Args:
            title: 任务标题
            project_id: 项目 ID
            content: 任务内容
            due_date: 截止日期
            priority: 优先级 (0-5)
            is_all_day: 是否为全天任务

        Returns:
            创建的任务
        """
        data = {
            "title": title,
            "projectId": project_id,
            "content": content,
            "isAllDay": is_all_day,
            "timeZone": self.timezone,
            "priority": priority
        }

        if due_date:
            data["dueDate"] = due_date

        return self._request("POST", "/task", json=data)

    def update_task(self, project_id: str, task_id: str, **kwargs) -> Dict[str, Any]:
        """
        更新任务

        Args:
            project_id: 项目 ID
            task_id: 任务 ID
            **kwargs: 更新的字段

        Returns:
            更新后的任务
        """
        return self._request("POST", f"/project/{project_id}/task/{task_id}", json=kwargs)

    def complete_task(self, project_id: str, task_id: str) -> Dict[str, Any]:
        """
        完成任务

        Args:
            project_id: 项目 ID
            task_id: 任务 ID

        Returns:
            操作结果
        """
        return self._request("POST", f"/project/{project_id}/task/{task_id}/complete")

    def delete_task(self, project_id: str, task_id: str) -> Dict[str, Any]:
        """
        删除任务

        Args:
            project_id: 项目 ID
            task_id: 任务 ID

        Returns:
            删除结果
        """
        return self._request("DELETE", f"/project/{project_id}/task/{task_id}")

    def search_tasks(self, project_id: str, title: str = "") -> List[Dict[str, Any]]:
        """
        搜索任务

        Args:
            project_id: 项目 ID
            title: 任务标题关键词

        Returns:
            匹配的任务列表
        """
        project_data = self.get_project_data(project_id)
        tasks = project_data.get("tasks", [])

        if not title:
            return tasks

        # 模糊搜索
        return [t for t in tasks if title.lower() in t.get("title", "").lower()]


def main():
    """测试代码"""
    # 使用示例
    client = Dida365Client("your_access_token_here")

    # 获取项目
    projects = client.get_projects()
    print(f"Projects: {len(projects)}")

    # 创建任务
    # task = client.create_task(
    #     title="测试任务",
    #     project_id="your_project_id",
    #     content="这是一个测试任务",
    #     priority=5
    # )
    # print(f"Task created: {task['id']}")


if __name__ == "__main__":
    main()
