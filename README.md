# Sample RAG MCP Server (HTTP)

**就業規則.docx ドキュメントを検索する RAG 機能を提供する MCP サーバー（Streamable HTTP 方式）**

このプロジェクトは、FastMCP を使用して HTTP 経由で RAG（Retrieval-Augmented Generation）機能を提供する MCP サーバーです。
就業規則のドキュメントから関連情報を検索し、質問に対する回答を生成します。

## 機能

- **search_work_rules**: 就業規則.docx ドキュメントから質問に関連する情報を検索するツール
- **Streamable HTTP 方式**: MCP クライアントから HTTP リクエストでアクセス可能
- **FAISS 検索**: 高速な類似性検索による関連文書の取得

## 環境要件

- Python 3.12 以上
- uv

## セットアップ

### 1. Git 設定

リポジトリをクローンした後、以下のコマンドを実行してください：

```bash
git config --global core.autocrlf false
```

※上記は、チェックアウト時、コミット時に改行コードを変更しない設定です（.gitattributes のままになります）

### 2. 仮想環境（.venv）の作成

仮想環境（`.venv`ディレクトリ）は GitHub リポジトリに登録されていないため、pull した後に仮想環境を作成する必要がある。

```コマンド（Windows Power Shell）
uv venv --python 3.12
```

※ `uv init`コマンドの実行は不要（pyproject.toml の作成などは作成済みのものが GitHub にプッシュされている）

### 3. .python-version の更新

```コマンド（Windows Power Shell）
uv python pin 3.12
```

※ `.python-version`が更新される。GitHub に登録されていない場合は新規作成される。

### 4. 依存関係のインストール

pyproject.toml に定義された依存関係をインストール：

```bash
uv sync
```

### 5. API サーバーの起動

API サーバーを起動してください（詳細は省略）。

## MCP クライアントからの接続

### 1. サーバー起動

まず MCP サーバーを起動します：

```powershell
# サーバー起動（ポート8001でリッスン）
uv run python rag_mcp_server_http.py
```

### 2. MCP クライアントからの利用

このサーバーは任意の MCP クライアントから利用できます。

**Claude Desktop から利用する場合の設定例：**

`claude_desktop_config.json`に以下のように設定：

```json
{
  "mcpServers": {
    "work-rules-http": {
      "transport": "streamable-http",
      "url": "http://127.0.0.1:8001/mcp"
    }
  }
}
```

**その他の MCP クライアントから利用する場合：**

- サーバー URL: `http://127.0.0.1:8001/mcp`
- トランスポート: `streamable-http`
- 利用可能ツール: `search_work_rules`

### 3. 利用方法

- **HTTP 方式**: サーバーが起動している間、任意の MCP クライアントから HTTP リクエストでアクセス可能
- **サーバー URL**: `http://127.0.0.1:8001/mcp`
- **利用可能ツール**: `search_work_rules`（就業規則ドキュメントの検索）

## 開発セットアップ

### 前提条件

- Python 3.11 以上
- [uv](https://docs.astral.sh/uv/) (Python パッケージマネージャー)
- Ollama（`nomic-embed-text:latest`モデル）

### セットアップ手順

**依存関係のインストール**

```powershell
# プロジェクトルートへ移動
cd D:\vscode_projects\sample_rag_mcp_server_http

# uvを使用して依存関係をインストール
uv sync
```

## Ollama 設定

使用モデル: `nomic-embed-text:latest`

## テスト実行

```powershell
# uvを使用してテストを実行
uv run pytest tests/ -v
```

## ファイル構成

```
sample_rag_mcp_server_http/
├── rag_mcp_server_http.py    # メインサーバーファイル
├── rag_core.py               # RAG検索ロジック
├── logger.py                 # ログ設定
├── pyproject.toml            # プロジェクト設定・依存関係
├── uv.lock                   # 依存関係ロックファイル
├── docs/                     # ドキュメント格納
│   └── 就業規則.docx
├── faiss_db/                 # FAISS検索インデックス
└── tests/                    # テストファイル
```
