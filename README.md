# CrewAI 多 Agent 协作示例

这是一个完整的 CrewAI 多智能体协作示例项目，展示了三个不同角色的 AI 智能体如何协作完成内容创作任务。

## 示例场景：内容创作团队

本示例模拟了一个博客文章创作团队，包含三个协作的 Agent：

1. **研究员** - 使用搜索工具收集最新的 AI 技术趋势信息
2. **写手** - 根据研究结果撰写一篇引人入胜的博客文章
3. **编辑** - 对文章进行校对和优化，输出最终成品

## 项目结构

```
my-crewai/
├── main.py           # 主程序，定义了所有 Agent 和 Task
├── pyproject.toml    # 项目依赖配置
├── .env.example      # 环境变量示例
└── output/           # 输出目录，最终文章会保存在这里
```

## 安装依赖

```bash
# 使用 uv 安装依赖（推荐）
uv sync

# 或者使用 pip
pip install -e .
```

## 配置 API 密钥

1. 复制 `.env.example` 到 `.env`:
```bash
cp .env.example .env
```

2. 在 `.env` 文件中填入你的 API 密钥：
- `OPENAI_API_KEY`: 你的 OpenAI API 密钥（必需）
- `SERPER_API_KEY`: Serper.dev API 密钥（用于网络搜索，在 [serper.dev](https://serper.dev/) 免费获取）

## 运行示例

```bash
python main.py
```

## 工作流程

程序采用**顺序执行**（Process.sequential）模式：

1. 研究员先执行，完成研究任务，输出研究报告
2. 写手基于研究员的输出，开始写作任务
3. 编辑基于写手的输出，完成最终编辑优化
4. 最终文章保存到 `output/final_blog_post.md`

## Agent 协作示意图

```
┌─────────────┐
│  研究员     │ ── 研究报告 → ┐
└─────────────┘               │
                              ▼
                        ┌─────────────┐
                        │   写手      │ ── 初稿 → ┐
                        └─────────────┘           │
                                                  ▼
                                          ┌─────────────┐
                                          │   编辑      │ ── 最终文章 → output/
                                          └─────────────┘
```

## 自定义修改

你可以修改 `main.py` 来：
- 更改 Agent 的角色和目标
- 修改任务描述
- 添加更多 Agent 协作
- 更换处理流程为层次化处理（Process.hierarchical）
- 添加更多工具

## 更多资源

- [CrewAI 官方文档](https://docs.crewai.com/)
- [CrewAI GitHub](https://github.com/crewaiinc/crewai)
