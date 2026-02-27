# Paper Servant 项目概览

Paper Servant 是一款基于 **Agno** 框架开发的、面向科研人员的自动化 AI 论文处理系统。系统采用 **Multi-Agent (多智能体)** 协作架构，实现了从 ArXiv 论文检索、自动化归类、深度阅读解读到知识问答的完整闭环。

## 1. 核心架构：Agent 角色与职责

系统设计遵循模块化与高内聚原则，由 Router 统一调度，多个 специализирован Agent 协同工作。

### 1.1 Router Agent (调度)
*   **名称**: `苍崎青子 (Router)`
*   **职责**:
    *   作为用户交互的主要入口。
    *   负责自然语言理解，将用户请求分发给其他专用 Agent。
    *   维护会话上下文（Context），处理多轮对话。
    *   管理系统级工具（如打开 PDF、查看笔记列表）。
*   **核心工具**: `SystemTools` (open_pdf, open_note), `MetadataTools` (check_local_paper)。

### 1.2 Paper Fetcher Agent (检索与下载)
*   **名称**: `FetcherAgent`
*   **职责**:
    *   对接 ArXiv API，执行关键词检索。
    *   根据规则（如最近两年、相关性排序）筛选论文。
    *   下载 PDF 文件并保存到本地 `papers/` 目录。
    *   记录论文元数据（Metadata）到 `papers/metadata.json`，包括标题、作者、摘要、引用数等。

### 1.3 Reader Agent (深度阅读)
*   **名称**: `久远寺有珠 (Reader)`
*   **职责**:
    *   读取本地 PDF 文件的全文本内容。
    *   深度分析论文结构（背景、方法、实验、结论）。
    *   生成标准化的中文阅读笔记（Markdown 格式），包含：
        *   摘要翻译
        *   研究背景与核心问题
        *   方法论详解
        *   实验结果与对比
        *   总结与局限性
    *   笔记保存至 `papers/notes/` 目录。

### 1.4 QA Agent (问答)
*   **名称**: `远坂凛 (QA)`
*   **职责**:
    *   针对**特定论文**进行深入问答。
    *   结合 PDF 原文和已生成的阅读笔记回答用户提问。
    *   记录每一次问答历史，作为后续知识积累的基础。

### 1.5 Organizer Agent (整理)
*   **名称**: `OrganizerAgent`
*   **职责**:
    *   扫描所有已下载论文的元数据。
    *   根据论文内容自动分类（如 LLM, Computer Vision, RL 等）。
    *   在 `papers/categorized/` 目录下创建分类文件夹和符号链接（不移动原始文件）。

### 1.6 Knowledge Agent (知识管理)
*   **名称**: `爱尔奎特 (Knowledge)`
*   **职责**:
    *   **通用知识问答**: 回答非特定论文的一般性 AI 概念问题。
    *   **Wiki 维护**: 将重要的概念定义、技术解释保存为 Markdown Wiki 文件。
    *   *(可选)* **向量检索**: 如果配置了 OpenAI 兼容的 Embedding 服务，可对 PDF 全文进行向量化索引和 RAG 检索。

## 2. 工具模块 (Tools)

系统通过工具类封装底层操作，供 Agent 调用。

*   **MetadataTools**:
    *   管理 `papers/metadata.json` 文件。
    *   提供论文的查找 (`find_paper`)、保存元数据 (`save_paper_metadata`)、获取所有论文列表功能。
*   **SystemTools**:
    *   跨平台打开文件。
    *   `open_pdf`: 调用系统默认阅读器打开 PDF。
    *   `open_note`: 调用系统默认编辑器（或指定应用如 Chrome）打开 Markdown 笔记。
*   **FileTools / PDFTools**:
    *   基础文件读写。
    *   PDF 文本提取与解析。
*   **WikiTools**:
    *   创建和检索 Wiki 知识条目。

## 3. 技术栈

*   **框架**: Agno (Agentic Framework)
*   **语言**: Python 3.12+
*   **模型接口**: OpenAI-Like API (默认配置为 ChatECNU / `ecnu-plus`)
*   **前端**: Next.js + Tailwind CSS (提供 Agent UI 界面)
*   **后端**: Python FastApi (通过 `playground.py` 暴露 AgentOS 服务)
*   **CLI**: Typer + Rich (命令行交互界面)
*   **数据存储**: 本地文件系统 (JSON Metadata, Markdown Notes) + *(可选)* LanceDB (Vector Store)

## 4. 工作流示例

一个典型的科研辅助流程如下：
1.  **用户**向 Router 发送指令："帮我找几篇关于 Agentic Workflow 的论文。"
2.  **Router** 调用 **Fetcher**，在 ArXiv 上检索并下载论文。
3.  **Router** 调用 **Organizer**，对下载的论文进行分类。
4.  **用户**指令："读一下第一篇，生成笔记。"
5.  **Router** 调用 **Reader**，读取 PDF 并生成中文笔记。
6.  **用户**指令："这篇论文的方法部分有什么创新？"
7.  **Router** 调用 **QA Agent**，基于笔记和原文回答问题。
