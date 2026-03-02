---
name: ticktick-sync
description: 滴答清单双向同步 Skill。支持中国版（dida365.com）和国际版（ticktick.com）。当用户说"添加待办"、"帮我记录"、"提醒我"等时，自动同步到滴答清单；当用户说"完成"、"标记完成"等时，自动标记滴答清单中对应任务为已完成。支持任务创建、完成、查询、优先级设置、项目分类等完整功能。基于官方 API 文档：https://developer.dida365.com/
---

# 滴答清单双向同步

## 概述

滴答清单同步 Skill 实现用户口头表达的待办事项与滴答清单（TickTick/滴答清单）之间的自动双向同步。支持中国版和国际版。通过自然语言识别用户意图，自动执行任务创建、完成、查询等操作。

## 版本支持

- ✅ **中国版**：https://dida365.com/ (API: api.dida365.com)
- ✅ **国际版**：https://ticktick.com/ (API: api.ticktick.com)

## 核心功能

### 1. 任务创建
- **触发关键词**：
  - "添加待办"
  - "帮我记录"
  - "提醒我"
  - "记一下"
  - "待办事项"
  - "todo"
  - "任务"
  
- **自动提取信息**：
  - 任务标题（必需）
  - 截止日期/时间
  - 优先级
  - 项目/列表
  - 标签
  - 描述

### 2. 任务完成
- **触发关键词**：
  - "完成"
  - "标记完成"
  - "完成了"
  - "搞定"
  - "done"
  - "finished"

- **匹配方式**：
  - 精确标题匹配
  - 模糊搜索
  - 最近任务匹配

### 3. 任务查询
- **触发关键词**：
  - "查看待办"
  - "有哪些任务"
  - "今天待办"
  - "任务列表"

### 4. 优先级管理
- **触发关键词**：
  - "紧急"、"重要"、"高优先级" → 优先级 5（高）
  - "中等"、"普通" → 优先级 3（中）
  - "不急"、"低优先级" → 优先级 1（低）

## 滴答清单 API 集成

### 认证方式

使用 **OAuth2 Bearer Token** 认证：

```
Authorization: Bearer <your_access_token>
```

**获取 Token**：
1. 登录滴答清单网页版（https://dida365.com/）
2. 按 F12 打开开发者工具
3. 切换到 Network 标签
4. 执行任意操作
5. 查找请求头中的 `Authorization` 字段值
6. 复制完整的 Token（格式：`dp_...`）

### 核心 API 端点

#### 1. 获取项目列表
```http
GET https://api.dida365.com/open/v1/project
Authorization: Bearer <token>
```

#### 2. 创建任务
```http
POST https://api.dida365.com/open/v1/task
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "任务标题",
  "projectId": "项目ID",
  "content": "任务内容",
  "isAllDay": true,
  "timeZone": "Asia/Shanghai",
  "priority": 5,
  "dueDate": "2026-03-03T15:00:00.000+08:00"
}
```

**优先级说明**：
- `5`: 高优先级（红色）
- `3`: 中优先级（橙色）
- `1`: 低优先级（蓝色）
- `0`: 无优先级（灰色）

#### 3. 完成任务
```http
POST https://api.dida365.com/open/v1/project/{projectId}/task/{taskId}/complete
Authorization: Bearer <token>
```

## 自然语言处理规则

### 日期时间解析

| 用户表达 | 解析结果 | API 格式 |
|---------|---------|---------|
| "明天下午3点" | 明天 15:00 | 2026-03-03T15:00:00.000+08:00 |
| "后天上午" | 后天 09:00 | 2026-03-04T09:00:00.000+08:00 |
| "下周三" | 下周三 00:00 | 2026-03-12T00:00:00.000+08:00 |

### 优先级解析

| 用户表达 | 优先级值 | 颜色 |
|---------|---------|------|
| "紧急"、"重要" | 5 | 🔴 红色 |
| "中等"、"普通" | 3 | 🟠 橙色 |
| "不急"、"低优先级" | 1 | 🔵 蓝色 |

## 使用示例

### 示例 1：简单任务创建
```
用户："添加待办：买牛奶"
AI："✅ 已创建待办：买牛奶（收件箱）"
```

### 示例 2：带时间的任务
```
用户："提醒我明天下午3点开会"
AI："✅ 已创建待办：开会
    📅 时间：明天 15:00
    📁 项目：收件箱"
```

### 示例 3：高优先级任务
```
用户："紧急！今天晚上之前完成报告"
AI："✅ 已创建待办：完成报告
    🔴 优先级：高
    📅 时间：今天 18:00"
```

## 错误处理

### 认证失败
```
❌ TickTick 认证失败，请检查 Access Token
→ 请重新配置 Token
```

### 任务不存在
```
❌ 未找到匹配的任务："xxx"
→ 请提供更精确的任务标题
```

## 最佳实践

### 1. 确认反馈
每次操作后，提供清晰的确认信息：
- ✅ 成功：显示任务详情
- ❌ 失败：说明原因和解决方案
- ⚠️ 警告：部分成功或需确认

### 2. 智能匹配
完成任务时：
1. 优先精确匹配标题
2. 其次模糊搜索
3. 最后匹配最近任务
4. 如有多个匹配，询问用户确认

### 3. 批量操作
支持批量操作场景：
- "完成今天的所有任务"
- "删除所有低优先级任务"
- "列出所有过期任务"

## 配置要求

### 必需配置
```json
{
  "ticktick": {
    "api_base": "https://api.ticktick.com/open/v1",
    "access_token": "your_access_token_here",
    "default_project_id": "inbox_project_id",
    "default_priority": 0
  }
}
```

## 技术实现

### 核心代码结构

```
ticktick-sync/
├── SKILL.md              # Skill 说明文档（本文件）
├── dida365_api.py        # 滴答清单 API 客户端
└── references/           # 参考文档
    └── dida365-api.md    # API 详细文档
```

### 使用 API 客户端

```python
from ticktick_sync.dida365_api import Dida365Client

# 创建客户端
client = Dida365Client(
    access_token="your_token",
    timezone="Asia/Shanghai"
)

# 获取项目
projects = client.get_projects()

# 创建任务
task = client.create_task(
    title="任务标题",
    project_id="项目ID",
    content="任务内容",
    priority=5
)

# 完成任务
client.complete_task(project_id, task_id)
```

## 相关资源

- **官方 API 文档**: https://developer.dida365.com/
- **滴答清单中国版**: https://dida365.com/
- **TickTick 国际版**: https://ticktick.com/

## 更新日志

### v2.0.0 (2026-03-02)
- ✅ 重构为支持滴答清单中国版
- ✅ 基于官方 API 文档实现
- ✅ 创建完整的 API 客户端
- ✅ 验证所有核心功能
- ✅ 更新配置为正确端点

### v1.0.0
- ✅ 初始版本（TickTick 国际版）
- ✅ 支持任务创建、完成、查询
- ✅ 自然语言解析
- ✅ 知识图谱集成