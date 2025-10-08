from fastmcp import FastMCP
import rag_core
from config import (
    SERVER_PORT,
    TOOL_NAME,
    TOOL_DESCRIPTION,
)

from logger import get_logger

# ロガー設定
logger = get_logger(__name__)

# サーバーをインスタンス化し、名前を付けます
mcp = FastMCP(name="mcp-server-http-02")

logger.info("FastMCPサーバーオブジェクト（Streamable HTTP）が作成されました。")


@mcp.tool(
    name=TOOL_NAME,
    description=TOOL_DESCRIPTION,
)
def search_temperature(prompt: str) -> str:
    logger.info(f"[1] 検索クエリ: {prompt}")

    results: list[str] = rag_core.search(prompt)

    logger.info(f"[2] 検索結果: {results}")

    return "\n\n".join(results)


if __name__ == "__main__":
    logger.info("--- __main__を介してFastMCPサーバーを開始 ---")
    # サーバーを起動します
    logger.info(f"サーバーをポート{SERVER_PORT}で起動します")
    mcp.run(transport="streamable-http", port=SERVER_PORT)
