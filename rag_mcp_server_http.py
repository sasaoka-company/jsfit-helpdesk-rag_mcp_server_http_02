from fastmcp import FastMCP
import rag_core

from logger import get_logger

# ロガー設定
logger = get_logger(__name__)

# サーバーをインスタンス化し、名前を付けます
mcp = FastMCP(name="work-rules-http")

logger.info("FastMCPサーバーオブジェクト（Streamable HTTP）が作成されました。")


@mcp.tool(
    name="search_work_rules",
    description="就業規則.docxドキュメントから質問に関連する情報を検索します。",
)
def search_work_rules(prompt: str) -> str:
    logger.info(f"[1] 検索クエリ: {prompt}")

    results: list[str] = rag_core.search(prompt)

    logger.info(f"[2] 検索結果: {results}")

    return "\n\n".join(results)


if __name__ == "__main__":
    logger.info("--- __main__を介してFastMCPサーバーを開始 ---")
    # サーバーを起動します（ポート8001でリッスンします）
    mcp.run(transport="streamable-http", port=8001)
