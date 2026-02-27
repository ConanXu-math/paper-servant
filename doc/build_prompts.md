# 从零搭建 Paper Servant 的 Prompt 清单

以下是一套按顺序使用的 Prompt，用于在 AI 辅助下从空目录一步步搭出与本项目同构的 Paper Servant。每个阶段 1～2 条，可直接复制发给 AI。

---

## 阶段 1：项目骨架

**Prompt 1**

> 用 Python 3.12+ 和 uv 新建一个 CLI 项目，名字叫 paper-servant。要 pyproject.toml、入口 main.py 用 Typer，先实现两个子命令：fetch 和 chat。依赖用 agno、typer、rich、python-dotenv。

**Prompt 2**

> 在这个项目里加 .env 支持，读取 LLM_API_KEY、LLM_BASE_URL、LLM_MODEL_ID。main.py 里 chat 命令要能调用一个 Agno Agent，用 OpenAILike 接这些环境变量。

---

## 阶段 2：ArXiv 与元数据

**Prompt 3**

> 加一个 tools/paper_tools.py：实现 search_arxiv 和 download_paper，用 ArXiv API，下载的 PDF 存到 papers/ 目录。再在 tools/metadata_tools.py 里实现 save_paper_metadata 和 get_all_papers，用 papers/metadata.json 存元数据。

**Prompt 4**

> 新建一个 Paper Fetcher Agent：根据用户 query 调用 search_arxiv、对每篇 download_paper、get_citation_count（可选）、save_paper_metadata，最后列出标题和引用数。把这个 Agent 接到 main.py 的 fetch 命令里。

---

## 阶段 3：读论文与笔记

**Prompt 5**

> 加 tools/pdf_tools.py：read_pdf(path) 用 PyPDF 提取正文。tools/file_tools.py 里实现 save_note(filename, content) 把 Markdown 存到 papers/notes/，以及 read_file。再实现 categorize_paper(paper_id, category, title) 在 papers/categorized/<category>/ 下做符号链接。

**Prompt 6**

> 新建 Reader Agent：先 get_all_papers 找论文，再 read_pdf 读内容，按固定 Markdown 模板生成中文阅读笔记（摘要、方法、实验、结论），用 save_note 保存，文件名要带 ArXiv ID。

**Prompt 7**

> 新建 QA Agent：根据 paper_id 读笔记或 PDF，回答用户问题，并在每次回答后调用 log_qa_session(paper_id, question, answer) 把问答写入 knowledge/qa_history/。

---

## 阶段 4：Router 与一站式对话

**Prompt 8**

> 新建 Router Agent：它不直接答问题，而是根据用户意图调用 Fetcher / Reader / QA / Organizer。工具包括：fetch_papers、organize_papers、read_paper(paper_id)、ask_paper_question(paper_id, question)、ask_general_question(question)、list_local_papers、open_note(paper_id)、open_pdf(paper_id)。用清晰的 instructions 规定：论文相关问题走 ask_paper_question，概念性问题走 ask_general_question，并记住上一篇讨论的 paper_id。

**Prompt 9**

> 把 main.py 的 chat 命令改成使用这个 Router Agent，并支持无参数时进入多轮交互（input 循环），输入 exit 退出。

---

## 阶段 5：知识库与 Web

**Prompt 10**

> 加 Knowledge Agent：用 WikiTools 做概念检索与写入，可选接向量库。Router 里 ask_general_question 委托给这个 Knowledge Agent。

**Prompt 11**

> 用 Agno 的 playground/AgentOS 方式启动 Router，提供 HTTP API（例如 7777 端口）。再给一个 Next.js 前端（或现成的 Agent UI）连 localhost:7777，能选 Agent、发消息、看回复。写一个 start_services.sh 同时启后端和前端。

---

## 阶段 6：体验与文档

**Prompt 12**

> 加一个工具：用户问「我有哪些文章」时，Router 调用 list_local_papers 列出 papers/ 下所有 PDF，并友好地总结给用户。

**Prompt 13**

> 加 ChatLogTools：每轮对话结束后把 (question, answer) 追加写入 logs/chat_sessions/chat_router.md，并在 Router 的 instructions 里要求每轮结束时调用一次。

**Prompt 14**

> 写 README：安装（uv sync）、配置 .env、运行方式（psv chat / start_services.sh）。再在 doc/ 下写 project_overview.md，说明各 Agent 职责、工具、技术栈和典型工作流。

---

## 使用说明

- 按 **1 → 14** 顺序执行，每完成一个阶段再发下一条。
- 若 AI 产出与现有项目结构不一致，可补充一句：「目录结构要和当前仓库一致，代码放在 agents/ 和 tools/ 下。」
- 熟练开发者配合这些 Prompt，整体从零到可运行约 **1～2 天**；纯手写约 **20～35 小时**。
