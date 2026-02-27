from pathlib import Path
from datetime import datetime
from agno.tools import Toolkit


class ChatLogTools(Toolkit):
    """
    简单的对话日志工具。
    
    用途：
    - 记录 Router 与用户之间的完整问答轮次
    - 日志文件保存在 logs/chat_sessions/ 目录下，按 session_label 分文件
    """

    def __init__(self, base_dir: str = "logs/chat_sessions"):
        super().__init__(name="chat_log_tools")
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # 注册工具函数
        self.register(self.log_chat_turn)

    def log_chat_turn(self, question: str, answer: str, session_label: str = "default") -> str:
        """
        记录一轮完整的问答。

        Args:
            question (str): 用户本轮的原始提问。
            answer (str): Router 汇总后的最终回答（可以是 Markdown）。
            session_label (str): 会话标签（例如 'router', 'paper_notes'），用于区分不同用途。

        Returns:
            str: 日志文件路径提示。
        """
        try:
            safe_label = "".join(c for c in session_label if c.isalnum() or c in ("_", "-")) or "default"
            log_file = self.base_dir / f"chat_{safe_label}.md"

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = (
                f"\n\n## [{timestamp}] Question\n"
                f"{question}\n\n"
                f"### Answer\n"
                f"{answer}\n\n"
                f"---\n"
            )

            mode = "a" if log_file.exists() else "w"
            with log_file.open(mode, encoding="utf-8") as f:
                f.write(entry)

            return f"Logged chat turn to {log_file}"
        except Exception as e:
            return f"Error logging chat turn: {e}"

