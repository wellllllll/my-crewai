#!/usr/bin/env python3
"""
CrewAI 多智能体协作示例 - 内容创作团队
========================================

这个示例展示了三个不同角色的 Agent 如何协作完成一篇博客文章的创作：
1. 研究员：收集最新的行业信息和趋势
2. 写手：根据研究结果撰写引人入胜的文章
3. 编辑：校对和优化文章内容

CrewAI 核心概念：
- Agent（智能体）：每个 Agent 有明确的 角色(role)、目标(goal)、背景故事(backstory)
- Task（任务）：每个任务分配给特定 Agent，包含描述和期望输出
- Crew（团队）：将多个 Agent 和 Task 组装在一起，定义执行流程
- Process（流程）：sequential（顺序执行）或 hierarchical（分层执行）
"""

import os
from dotenv import load_dotenv
# 导入 CrewAI 核心类
from crewai import Agent, Crew, Task, Process
# 导入 CrewAI 预置工具
from crewai_tools import SerperDevTool, WebsiteSearchTool

# ========== 第一步：加载环境变量 ==========
# 必须在任何操作之前加载，确保工具能读取到 API 密钥
load_dotenv()


class ContentCreationCrew:
    """
    内容创作团队
    ==========

    这是一个由三个不同角色 Agent 组成的协作团队：
    - 研究员 -> 写手 -> 编辑，顺序完成内容创作全流程
    """

    def __init__(self):
        """
        初始化团队：在环境变量加载之后初始化工具
        为什么要在这里初始化工具？
        - 确保 load_dotenv() 已经执行完成，工具能读取到环境变量中的 API 密钥
        - 条件加载：如果没有配置 SERPER_API_KEY，程序依然可以运行（只是无法搜索）
        """
        # 存储可用工具的列表
        self.tools = []

        # 如果配置了 Serper API Key，才初始化搜索工具
        # SerperDevTool: 用于 Google 搜索，获取最新网络信息
        if os.getenv("SERPER_API_KEY"):
            self.search_tool = SerperDevTool()
            self.tools.append(self.search_tool)

            # WebsiteSearchTool: 用于读取网站内容，进行 RAG 检索
            # 需要 OPENAI_API_KEY 来处理嵌入向量
            self.web_search_tool = WebsiteSearchTool()
            self.tools.append(self.web_search_tool)

    # ========== 定义 Agent 1: 研究员 ==========
    def researcher(self) -> Agent:
        """
        创建研究员 Agent

        Agent 的三个核心属性：
        - role: 明确的角色定位，让 AI 知道自己该扮演谁
        - goal: 具体目标，告诉 AI 要达成什么结果
        - backstory: 背景故事，赋予 AI 身份和性格，影响输出风格
        """
        return Agent(
            # 角色：明确这是什么身份
            role="技术行业研究员",
            # 目标：这个角色要完成什么任务
            goal="收集最新的 AI 技术趋势和发展动态，提供有洞察力的分析",
            # 背景故事：塑造角色的经验和特点，帮助 AI 更好理解自己的职责
            backstory="""你是一位经验丰富的技术行业研究员，
            擅长追踪人工智能领域的最新发展。你拥有敏锐的洞察力，
            能够从海量信息中提炼出真正有价值的趋势和观点。""",
            # 工具：赋予 Agent 能力，这里绑定了搜索工具
            # 如果没有配置 SERPER_API_KEY，tools 是空列表，Agent 会基于自身知识回答
            tools=self.tools,
            # verbose: 是否输出详细思考过程，方便调试
            verbose=True,
            # allow_delegation: 是否允许委托任务给其他 Agent
            # 这里设为 False，因为每个任务都明确分配好了
            allow_delegation=False
        )

    # ========== 定义 Agent 2: 写手 ==========
    def writer(self) -> Agent:
        """创建写手 Agent - 根据研究结果撰写文章"""
        return Agent(
            role="技术内容创作者",
            goal="根据研究资料撰写一篇引人入胜、信息丰富的技术博客文章",
            backstory="""你是一位专业的技术博主，擅长将复杂的技术概念
            转化为通俗易懂的内容。你的写作风格生动有趣，能够吸引
            普通读者理解前沿技术话题。""",
            # 写手不需要搜索工具，只需要基于研究员的输出写作
            verbose=True,
            allow_delegation=False
        )

    # ========== 定义 Agent 3: 编辑 ==========
    def editor(self) -> Agent:
        """创建编辑 Agent - 对文章进行校对优化"""
        return Agent(
            role="内容编辑",
            goal="校对并优化文章，确保内容流畅、结构清晰、没有错误",
            backstory="""你是一位经验丰富的编辑，对文字质量有严格要求。
            你擅长优化文章结构，改善表达方式，并确保最终稿件没有
            语法错误和拼写错误。""",
            verbose=True,
            allow_delegation=False
        )

    # ========== 定义 Task 1: 研究任务 ==========
    def research_task(self) -> Task:
        """
        定义研究任务 - 分配给研究员

        Task 的核心属性：
        - description: 详细描述任务要求，越具体越好
        - expected_output: 明确期望输出格式，让 AI 知道输出应该长什么样
        - agent: 将任务分配给哪个 Agent
        """
        return Task(
            # 任务描述：尽可能详细，告诉 Agent 具体要做什么
            description="""
                研究当前人工智能领域最热门的三个技术趋势。
                重点关注 2024-2025 年的最新发展。
                对于每个趋势，请提供：
                1. 趋势名称和简要介绍
                2. 为什么这个趋势重要
                3. 对行业的影响
                4. 未来发展展望

                请确保信息是最新的，并提供关键数据支撑你的结论。
                最终输出一份详细的研究报告。
            """,
            # 期望输出：明确告诉 AI 你期望得到什么结果
            expected_output="一份关于 AI 三大热门趋势的详细研究报告，包含每个趋势的介绍、重要性、影响和展望",
            # 将此任务分配给研究员 Agent
            agent=self.researcher()
        )

    # ========== 定义 Task 2: 写作任务 ==========
    def writing_task(self) -> Task:
        """定义写作任务 - 分配给写手

        重要：写作任务会自动获得前一个任务（研究任务）的输出作为上下文
        研究员产出的研究报告会自动传给写手作为参考资料
        """
        return Task(
            description="""
                根据研究员提供的研究报告，撰写一篇博客文章。
                文章标题要吸引眼球，内容结构要清晰：
                - 引言：为什么现在讨论 AI 趋势很重要
                - 每个趋势单独分段讲解
                - 总结：对开发者和企业的建议

                文章要求：
                - 字数在 800-1200 字
                - 语言通俗易懂，适合技术开发者阅读
                - 标题使用 markdown 格式
                - 每个趋势要有清晰的小标题

                使用研究员提供的信息，但要用自己的话表达。
            """,
            expected_output="一篇完整的 markdown 格式博客文章，结构清晰，语言流畅",
            # 将此任务分配给写手 Agent
            agent=self.writer()
        )

    # ========== 定义 Task 3: 编辑任务 ==========
    def editing_task(self) -> Task:
        """定义编辑任务 - 分配给编辑

        output_file: CrewAI 会自动将最终输出写入指定文件
        """
        return Task(
            description="""
                校对并优化写手撰写的博客文章：
                1. 检查语法和拼写错误
                2. 改善句子流畅度
                3. 确保段落过渡自然
                4. 优化标题和小标题
                5. 保持原文的核心观点和内容不变

                输出最终完善后的完整文章。
            """,
            expected_output="经过编辑优化后的最终博客文章，格式为完整的 markdown",
            agent=self.editor(),
            # output_file: 自动将最终结果保存到这个文件
            output_file="output/final_blog_post.md"
        )

    # ========== 组装 Crew ==========
    def crew(self) -> Crew:
        """
        组装 Crew（团队）

        Crew 是 CrewAI 的核心概念，它：
        1. 管理所有 Agent
        2. 管理所有 Task
        3. 按照指定的 Process 执行任务
        4. 处理任务之间的上下文传递
        """
        return Crew(
            # 团队包含哪些 Agent，顺序影响执行（但任务自己绑定了 Agent，所以影响不大）
            agents=[
                self.researcher(),
                self.writer(),
                self.editor()
            ],
            # 任务列表，这个顺序很重要！Process.sequential 会按这个顺序执行
            tasks=[
                self.research_task(),   # 第一步：研究员做研究
                self.writing_task(),    # 第二步：写手写文章
                self.editing_task()     # 第三步：编辑做校对
            ],
            # Process: 执行流程
            # - Process.sequential: 按顺序一个接一个执行，前一个完成后才会开始下一个
            # - Process.hierarchical: 分层模式，有一个管理者分配任务给工人，适合更复杂的场景
            process=Process.sequential,
            # verbose: 是否输出详细执行过程
            verbose=True
        )


def main():
    """
    主函数：运行多 Agent 协作示例

    执行流程：
    1. 检查环境变量配置
    2. 创建 ContentCreationCrew 对象（初始化 Agent 和工具）
    3. 调用 crew.kickoff() 启动执行
    4. 输出最终结果
    """
    # 检查环境变量
    if not os.getenv("OPENAI_API_KEY"):
        print("错误: 请设置 OPENAI_API_KEY 环境变量")
        print("你可以在 .env 文件中添加 OPENAI_API_KEY=your_key")
        return

    print("============================================")
    print("  CrewAI 多智能体协作示例 - 内容创作团队")
    print("============================================")
    print("\n开始执行任务，三个 Agent 将协作完成一篇 AI 趋势博客文章...\n")

    # ========== 关键：创建并启动 Crew ==========
    # 1. 创建 ContentCreationCrew 实例
    # 2. 调用 .crew() 得到组装好的 Crew 对象
    # 3. 调用 .kickoff() 开始执行，返回最终结果
    content_crew = ContentCreationCrew().crew()
    result = content_crew.kickoff()

    print("\n============================================")
    print("  任务完成！输出文件: output/final_blog_post.md")
    print("============================================")
    print("\n最终结果:")
    print(result)


if __name__ == "__main__":
    main()
