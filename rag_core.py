# rag_core.py
import os
from dotenv import load_dotenv
import glob

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from config import EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, DEFAULT_TOP_K
from logger import get_logger

# ロガー設定
logger = get_logger(__name__)

# 環境変数ロード
load_dotenv()

# ベースディレクトリ設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Embedding モデル（Ollamaを使用）
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

# PDF読み込み & DOCX対応 & チャンク化
pdf_dir = os.path.join(BASE_DIR, "docs")
# 対象拡張子を指定
pdf_paths = sorted(glob.glob(os.path.join(pdf_dir, "*.pdf")))
docx_paths = sorted(glob.glob(os.path.join(pdf_dir, "*.docx")))

if not (pdf_paths or docx_paths):
    raise FileNotFoundError(f"No PDF or DOCX files found in {pdf_dir}")

all_raw_docs = []

# PDF読み込み
for path in pdf_paths:
    logger.info(f"Loading PDF: {path}")
    loader = PyPDFLoader(path)
    docs_part = loader.load()
    all_raw_docs.extend(docs_part)

# DOCX読み込み（PoC: Unstructured を必須とする）
for path in docx_paths:
    logger.info(f"Loading DOCX: {path}")
    loader = UnstructuredWordDocumentLoader(path)
    docs_part = loader.load()
    all_raw_docs.extend(docs_part)

raw_docs = all_raw_docs

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)
docs = text_splitter.split_documents(raw_docs)


# ベクトルDB作成（FAISSを使用）
faiss_path = os.path.join(BASE_DIR, "faiss_db")
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
    logger.info(f"① 検索クエリ: {prompt}")

    # FAISS に直接問い合わせ
    docs = vectorstore.similarity_search(prompt, k=DEFAULT_TOP_K)
    logger.info(f"② 取得ドキュメント: {docs}")

    # 検索結果をテキストとして抽出
    result = [doc.page_content for doc in docs]
    logger.info(f"③ 検索結果: {result}")

    return result
