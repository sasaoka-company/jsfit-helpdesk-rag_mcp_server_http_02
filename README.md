**RAG 機能を提供する MCP サーバー（Streamable HTTP 方式）その２**

このプロジェクトは、PDF/DOCX ドキュメントから関連情報を検索し、RAG（Retrieval-Augmented Generation）機能を提供する MCP サーバーです。
HTTP 通信を通じて MCP クライアントとの通信を行います。

# 1. 機能

- **Streamable HTTP 方式**: MCP クライアントから HTTP 通信によりアクセス
- **ベクトル DB 検索**: 高速な類似性検索による関連文書の取得

# 2. 前提条件

- Python 3.12 以上
- [uv](https://docs.astral.sh/uv/) (Python パッケージマネージャー)
- モデル実行環境：Ollama
- Embedding モデル：`nomic-embed-text:latest`
- 仮想環境（`.venv`）が作成されていること

# 3. MCP クライアントからの接続

- コマンド: `（プロジェクトルート）\.venv\Scripts\python.exe`
- 実行スクリプト: `src\rag_mcp_server_http_02.py`
- トランスポート: `streamable-http`

## （参考）Claude Desktop から利用する場合の設定例：

`claude_desktop_config.json`に以下のように設定：

```json
{
  "mcpServers": {
    "mcp-server-http-02": {
      "transport": "streamable-http",
      "url": "http://127.0.0.1:8002/mcp"
    }
  }
}
```

# 4. 開発環境セットアップ

## 4-1. Git 設定

以下コマンドにより、チェックアウト時、コミット時に改行コードを変更しないようにします。（`.gitattributes` のままになります）

```powershell
git config --global core.autocrlf false
```

## 4-2. 依存関係のインストール

以下コマンドにより、`pyproject.toml`で定義されているライブラリをインストールします。

```powershell
uv sync
```

# 5. MCP サーバ起動

```powershell
$env:PYTHONPATH = "." ; uv run python src/rag_mcp_server_http_02.py
```

※ 標準入出力方式の場合は明示的な MCP サーバの起動は不要ですが、Streamable HTTP 方式の MCP サーバは起動する必要があります。

# 6. テスト実行

```powershell
uv run pytest tests/ -v
```

# 7. その他

## 7-1. Embedding モデルを切り替える

以下変更箇所のコメントアウトを切り替える。

- `.env`
  OPENAI_API_BASE
  OPENAI_API_KEY

※ Ollama を使わない場合は`OPENAI_API_BASE`定数はコメントアウトして無効にする

- `config.py`
  EMBEDDING_MODEL

- `rag_core.py`
  from langchain_ollama import OllamaEmbeddings # Ollama Embeddings
  from langchain_openai import OpenAIEmbeddings # OpenAI Embeddings

  embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
  embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
