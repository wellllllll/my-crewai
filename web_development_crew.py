#!/usr/bin/env python3
"""
CrewAI 多智能体协作开发 Web 项目示例
========================================

这个示例展示了软件开发团队中不同角色如何协作开发一个网页：
1. 产品经理：分析需求，定义产品功能和页面结构
2. 前端工程师：根据需求文档实现 HTML/CSS/JavaScript 页面
3. 代码评审：检查代码质量，提出改进建议
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Task, Process

# 加载环境变量
load_dotenv()


class WebDevelopmentCrew:
    """Web 开发团队 - 多 Agent 协作开发网页"""

    def product_manager(self) -> Agent:
        """产品经理 Agent - 负责需求分析和功能定义"""
        return Agent(
            role="资深产品经理",
            goal="分析用户需求，输出清晰的产品需求文档和页面设计规范",
            backstory="""你有10年互联网产品经验，擅长将模糊的用户需求
            转化为清晰具体的产品规格。你非常注重用户体验，能够设计出
            结构清晰、交互简单的页面结构。""",
            verbose=True,
            allow_delegation=False
        )

    def frontend_developer(self) -> Agent:
        """前端开发工程师 Agent - 负责实现网页代码"""
        return Agent(
            role="前端开发工程师",
            goal="根据产品需求文档，写出高质量的 HTML/CSS/JavaScript 代码",
            backstory="""你是一名经验丰富的前端开发工程师，精通 HTML5、CSS3、JavaScript。
            你擅长编写简洁、可维护的代码，能够实现美观的页面布局和响应式设计。
            你熟悉现代前端设计原则，喜欢使用 Tailwind CSS 风格的样式写法。""",
            verbose=True,
            allow_delegation=False
        )

    def code_reviewer(self) -> Agent:
        """代码评审 Agent - 负责检查代码质量"""
        return Agent(
            role="高级前端工程师 / 代码评审",
            goal="检查代码质量，发现潜在问题，提出改进建议，确保代码高质量",
            backstory="""你是团队中的技术负责人，对代码质量有严格要求。
            你擅长检查 HTML 结构是否合理、CSS 是否简洁、JavaScript 是否优雅。
            你会提出具体的改进建议，帮助团队产出高质量代码。""",
            verbose=True,
            allow_delegation=False
        )

    def requirement_analysis_task(self) -> Task:
        """需求分析任务 - 产品经理完成"""
        return Task(
            description="""
                用户需要创建一个"个人开发者作品集"展示页面。
                页面需要展示开发者的基本信息、技能栈、项目作品和联系方式。

                请你完成：
                1. 设计页面整体结构（分几个区块，每个区块放什么内容）
                2. 确定页面配色方案和整体风格（建议现代化简约风格）
                3. 列出需要的功能和交互效果
                4. 输出一份详细的产品需求文档，让前端开发可以直接按照文档编码

                页面要求：
                - 响应式设计，适配手机和电脑
                - 现代化美观的设计
                - 包含：个人介绍、技能、项目列表、联系方式四个主要部分
                - 添加简单的交互动画效果

                请用中文输出完整的需求文档。
            """,
            expected_output="一份完整的产品需求文档，包含页面结构、设计规范、功能需求",
            agent=self.product_manager()
        )

    def coding_task(self) -> Task:
        """编码任务 - 前端工程师完成"""
        return Task(
            description="""
                根据产品经理输出的需求文档，实现一个完整的 HTML 页面。

                要求：
                1. 使用纯 HTML + CSS + JavaScript，不需要引入框架
                2. 内联所有 CSS 样式，不要分开 CSS 文件，单文件 HTML
                3. 实现响应式布局，适配桌面和移动设备
                4. 添加适当的动画和交互效果
                5. 代码要简洁清晰，有良好的缩进和结构

                直接输出完整的 HTML 代码即可，包含所有内容。
                最终页面应该是一个可以直接在浏览器打开的静态 HTML 文件。
            """,
            expected_output="完整的 HTML 代码，包含所有 CSS 和 JavaScript，单个文件",
            agent=self.frontend_developer(),
        )

    def code_review_task(self) -> Task:
        """代码评审任务 - 代码评审完成"""
        return Task(
            description="""
                评审前端工程师写出的 HTML 代码：
                1. 检查 HTML 结构是否语义化合理
                2. 检查 CSS 是否简洁，有没有可以优化的地方
                3. 检查 JavaScript 是否简洁高效
                4. 检查是否满足产品需求
                5. 如果发现问题，直接修正代码，输出改进后的完整代码

                如果代码质量没问题，也请输出最终确认过的完整代码。
                最终输出应该是完整可运行的 HTML 代码，可以直接保存打开。
            """,
            expected_output="经过评审和优化后的完整 HTML 代码，可直接运行",
            agent=self.code_reviewer(),
            output_file="dist/portfolio.html"
        )

    def crew(self) -> Crew:
        """组装 Web 开发团队"""
        return Crew(
            agents=[
                self.product_manager(),
                self.frontend_developer(),
                self.code_reviewer()
            ],
            tasks=[
                self.requirement_analysis_task(),  # 第一步：需求分析
                self.coding_task(),                # 第二步：编写代码
                self.code_review_task()            # 第三步：代码评审
            ],
            process=Process.sequential,
            verbose=True
        )


def main():
    """运行 Web 开发团队协作示例"""
    # 检查环境变量
    if not os.getenv("OPENAI_API_KEY"):
        print("错误: 请设置 OPENAI_API_KEY 环境变量")
        print("你可以在 .env 文件中添加 OPENAI_API_KEY=your_key")
        return

    print("============================================")
    print("  CrewAI 多智能体协作示例 - Web 开发团队")
    print("============================================")
    print("\n开始执行，三个 Agent 将协作开发一个个人作品集页面...\n")

    # 创建团队并启动
    dev_crew = WebDevelopmentCrew().crew()
    result = dev_crew.kickoff()

    print("\n============================================")
    print("  开发完成！输出文件: dist/portfolio.html")
    print("============================================")
    print("\n最终结果:")
    print(result)


if __name__ == "__main__":
    main()
