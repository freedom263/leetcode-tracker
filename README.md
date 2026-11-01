# LeetCode Tracker

> 一个帮助你分析和追踪 LeetCode 刷题进度的命令行工具

## 为什么做这个项目？

作为一名准备秋招的计算机专业学生，我每天都在刷 LeetCode，但发现：
- 不知道自己刷题的薄弱环节在哪里
- 缺乏对刷题进度的量化分析
- 想要更直观地看到自己的成长曲线

于是决定做一个工具，通过 LeetCode API 获取自己的刷题数据，进行可视化分析。

## 功能规划

### MVP（第 1 周）
- [x] 项目初始化
- [ ] 通过 LeetCode API 获取用户刷题数据
- [ ] 命令行显示基础统计（总题数、通过率、难度分布）
- [ ] 保存数据到本地 JSON

### 后续功能
- [ ] 按标签分析（数组、链表、动态规划等）
- [ ] 生成刷题热力图
- [ ] 题目推荐（基于薄弱环节）
- [ ] 导出数据到 Markdown/Excel

## 技术栈

- **语言**：Python 3.8+
- **核心库**：
  - `requests` - API 调用
  - `rich` - 命令行美化
  - `click` - CLI 框架
- **数据存储**：JSON（后续考虑 SQLite）

## 快速开始

```bash
# 克隆项目
git clone https://github.com/your-username/leetcode-tracker.git
cd leetcode-tracker

# 安装依赖
pip install -r requirements.txt

# 运行
python main.py --username your-leetcode-username
```

## 项目结构

```
leetcode-tracker/
├── main.py              # 入口文件
├── api/
│   └── leetcode.py      # LeetCode API 封装
├── analyzer/
│   └── stats.py         # 数据分析逻辑
├── utils/
│   └── storage.py       # 数据存储
├── requirements.txt     # 依赖
└── README.md
```

## 开发日志

- **2026-11-01**：项目启动，确定技术方案

## License

MIT
