from typing import Optional, List
from agno.agent import Agent
from agno.models.openai import OpenAILike
from tools.wiki_tools import WikiTools
from tools.file_tools import FileTools
import os
from dotenv import load_dotenv

load_dotenv()


def get_knowledge_agent(model_id: str = "gpt-4o"):
    """
    Returns an Agent configured to manage and retrieve general AI knowledge.
    Uses Vector Database (LanceDB) for semantic search over papers and notes.
    """
    
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model_name = os.getenv("LLM_MODEL_ID", model_id)
    
    # 当前安装的 agno 版本不包含 `agno.knowledge.pdf` 模块，
    # 因此这里暂时只提供基于 Wiki 和本地文件的知识管理能力，
    # 不启用 PDF 向量数据库，以保证项目可以正常运行。

    return Agent(
        name="爱尔奎特 (Knowledge)",
        model=OpenAILike(
            id=model_name,
            api_key=api_key,
            base_url=base_url
        ),
        tools=[WikiTools(), FileTools()],
        description="You are the Librarian and Knowledge Manager of the Paper Servant system.",
        instructions=[
            "You have two main responsibilities:",
            "1. **Answer General Questions**: Based on existing knowledge (wiki, paper notes, Q&A history).",
            "2. **Maintain Knowledge Base (Wiki)**: Store definitions of fundamental concepts using the wiki tools.",
            "**Language**: Use professional Chinese unless requested otherwise."
        ],
        markdown=True,
    )
