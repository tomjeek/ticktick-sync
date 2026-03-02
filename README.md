# ticktick-sync

滴答清单双向同步 Skill - 支持中国版和国际版

## Features

- 🚀 Dual version support (CN/Global)
- 📝 Task management (create, complete, update, delete)
- 🎯 Priority levels
- 📅 Due dates and all-day tasks
- 🔍 Task search
- 🌍 Timezone support
- 📚 Knowledge graph integration

## Quick Start

### Installation

```bash
git clone https://github.com/tomjeek/ticktick-sync.git
cd ticktick-sync
```

### Configuration

1. Get your TickTick Access Token from https://dida365.com/
2. Configure the API client:

```python
from dida365_api import Dida365Client

client = Dida365Client(
    access_token="your_token",
    timezone="Asia/Shanghai"
)

# Create a task
task = client.create_task(
    title="Task title",
    project_id="project_id",
    content="Task description",
    priority=5
)

# Complete a task
client.complete_task(
    project_id="project_id",
    task_id="task_id"
)
```

### Natural Language Usage

```
"添加待办：买牛奶"
"提醒我明天下午3点开会"
"紧急！今天晚上之前完成报告"
"完成买牛奶"
"查看今天的待办事项"
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/project` | GET | Get project list |
| `/project/{id}` | GET | Get project details |
| `/project/{id}/data` | GET | Get project and tasks |
| `/project` | POST | Create project |
| `/project/{id}/task` | POST | Create task |
| `/project/{id}/task/{id}` | POST | Complete task |
| `/project/{id}/task/{id}` | DELETE | Delete task |

## Priority Levels

| Value | Priority | Color |
|-------|----------|-------|
| 5 | High | 🔴 Red |
| 3 | Medium | 🟠 Orange |
| 1 | Low | 🔵 Blue |
| 0 | None | ⚪ Gray |

## Project Structure

```
ticktick-sync/
├── README.md             # Project readme
├── SKILL.md              # Skill documentation
├── dida365_api.py        # API client
├── agents/               # UI metadata
│   └── openai.yaml
├── scripts/              # Executable scripts
│   ├── dida365_api.py
│   ├── nlp_parser.py
│   └── ticktick_api.py
└── references/           # Reference docs
    ├── config-guide.md
    └── dida365-api.md
```

## Links

- Website: https://dida365.com/
- TickTick Global: https://ticktick.com/
- API Documentation: https://developer.dida365.com/
- memU Bot: https://github.com/tomjeek/memu-bot

## License

MIT License - see LICENSE file for details

## Version

v2.0.0 - 2026-03-02

---

Made with ❤️ by memU Bot