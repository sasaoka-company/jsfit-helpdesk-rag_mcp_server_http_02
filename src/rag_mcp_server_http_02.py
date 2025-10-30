import sys
import os
import json

from fastmcp import FastMCP
from src.rag_core import search
from src.config import (
    SERVER_PORT,
    TOOL_NAME,
    TOOL_DESCRIPTION,
)

from logger import get_logger

# ロガー設定
logger = get_logger(__name__)

logger.info("=== SERVER STARTED ===")
logger.info("sys.executable: %s", sys.executable)
logger.info("sys.prefix: %s", sys.prefix)
logger.info("PATH: %s", os.environ.get("PATH"))

# サーバーをインスタンス化し、名前を付けます
mcp = FastMCP(name="mcp-server-http-02")

logger.info("FastMCPサーバーオブジェクト（Streamable HTTP）が作成されました。")


@mcp.tool(
    name=TOOL_NAME,
    description=TOOL_DESCRIPTION,
)
def search_temperature(prompt: str) -> str:
    logger.info(f"[1] 検索クエリ: {prompt}")

    results: list[str] = search(prompt)

    logger.info(f"[2] 検索結果: {results}")

    # MCPではJSON-RPC 2.0で通信するため、Pythonのlistやdictをそのまま返すと
    # JSON文字列にシリアライズする処理が **自動的に** 実行されるため、基本的に制御できない。
    # このシリアライズ処理を制御するため、**明示的に** JSON文字列に変換して返す。
    #
    # JSON-RPC 2.0 レスポンス上では次のように "result" の値としてシリアライズされる:
    # （例）
    # {
    #   "jsonrpc": "2.0",
    #   "id": 12345,
    #   "result": "[\"結果１\", \"結果２\"]"  # ← JSON文字列として格納される
    # }
    #
    # 戻り値: str（JSON文字列形式の結果リスト）
    # MCPクライアント側で json.loads(result) によりリストへ復元できる。
    return json.dumps(results, ensure_ascii=False)


if __name__ == "__main__":
    logger.info("--- __main__を介してFastMCPサーバーを開始 ---")
    # サーバーを起動します
    logger.info(f"サーバーをポート{SERVER_PORT}で起動します")
    mcp.run(transport="streamable-http", port=SERVER_PORT)
