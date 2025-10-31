# rag_core.py
import csv
import os
from dotenv import load_dotenv
import glob

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import CSVLoader

from langchain.schema import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_ollama import OllamaEmbeddings  # Ollama Embedding
from langchain_openai import OpenAIEmbeddings  # OpenAI Embedding

from langchain_community.vectorstores import FAISS
from src.config import (
    ROOT_DIR,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    DEFAULT_TOP_K,
)
from src.logger import get_logger

# ロガー設定
logger = get_logger(__name__)

# 環境変数ロード
load_dotenv()

# Embedding モデル
embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
# embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

# PDF、DOCX、TXT、CSV読み込み、チャンク化
docs_dir = os.path.join(ROOT_DIR, "docs")
# 対象拡張子を指定
pdf_paths = sorted(glob.glob(os.path.join(docs_dir, "*.pdf")))
docx_paths = sorted(glob.glob(os.path.join(docs_dir, "*.docx")))
txt_paths = sorted(glob.glob(os.path.join(docs_dir, "*.txt")))
csv_paths = sorted(glob.glob(os.path.join(docs_dir, "*.csv")))

if not (pdf_paths or docx_paths or txt_paths or csv_paths):
    raise FileNotFoundError(f"No PDF, DOCX, TXT or CSV files found in {docs_dir}")

all_raw_docs = []

# PDF
for path in pdf_paths:
    logger.info(f"Loading PDF: {path}")
    loader = PyPDFLoader(path)
    docs_part = loader.load()
    all_raw_docs.extend(docs_part)

# DOCX（PoC: Unstructured を必須とする）
for path in docx_paths:
    logger.info(f"Loading DOCX: {path}")
    loader = UnstructuredWordDocumentLoader(path)
    docs_part = loader.load()
    all_raw_docs.extend(docs_part)

# TXT
for path in txt_paths:
    logger.info(f"Loading TXT: {path}")
    loader = TextLoader(path, encoding="utf-8")
    docs_part = loader.load()
    all_raw_docs.extend(docs_part)

# CSV
for path in csv_paths:
    logger.info(f"Loading CSV: {path}")
    # CSVLoaderは列をテキストとしてまとめて読み込む
    loader = CSVLoader(file_path=path, encoding="utf-8")
    docs_part = loader.load()
    all_raw_docs.extend(docs_part)
    # logger.info(f"Loading CSV: {path}")

    # docs_part = []
    # with open(path, "r", encoding="utf-8") as f:
    #     reader = csv.DictReader(f)
    #     for row in reader:
    #         # 各セルを " | " 区切りで結合して1つの文字列にする
    #         text = " | ".join(str(v) for v in row.values() if v and str(v).strip())
    #         if text.strip():
    #             docs_part.append(Document(page_content=text, metadata={"source": path}))

    # all_raw_docs.extend(docs_part)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)
docs = text_splitter.split_documents(all_raw_docs)


# ベクトルDB作成（FAISSを使用）
faiss_path = os.path.join(ROOT_DIR, "faiss_db")
if os.path.exists(faiss_path):
    vectorstore = FAISS.load_local(
        faiss_path, embeddings, allow_dangerous_deserialization=True
    )
else:
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(faiss_path)


# 検索+回答関数
def search(prompt: str) -> list[str]:
    """
    ベクトルデータベースを検索します。
    """
    try:
        logger.info("=== search START")
        logger.info(f"prompt: {prompt}")

        logger.info(f"① 検索クエリ: {prompt}")

        # FAISS に直接問い合わせ
        docs = vectorstore.similarity_search(prompt, k=DEFAULT_TOP_K)
        logger.info(f"② 取得ドキュメント: {docs}")

        # 検索結果をテキストとして抽出
        result: list[str] = [doc.page_content for doc in docs]
        logger.info(f"③ 検索結果: {result}")

        return result

    except Exception as e:
        logger.error(f"search エラー: {e}")
        logger.exception(e)
        raise
    finally:
        logger.info("=== search END ===")
