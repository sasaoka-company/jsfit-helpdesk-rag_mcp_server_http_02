import os
import sys

# ensure project root is on sys.path
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.rag_core import search
from src.config import DEFAULT_TOP_K, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP


def test_search_returns_list_and_max_top_k():
    """Smoke test: search() returns a list of strings with length <= DEFAULT_TOP_K."""
    # use a simple prompt; behavior depends on data in docs/
    result = search("テスト")
    assert isinstance(result, list)
    assert all(isinstance(r, str) for r in result)
    assert len(result) <= DEFAULT_TOP_K


def test_search_with_specific_query():
    """Test search with a more specific query related to the document content."""
    result = search("気温")
    assert isinstance(result, list)
    assert len(result) >= 0  # may be empty if no relevant content found
    assert len(result) <= DEFAULT_TOP_K


def test_search_with_empty_query():
    """Test search behavior with empty query."""
    result = search("")
    assert isinstance(result, list)
    assert len(result) <= DEFAULT_TOP_K


def test_config_constants():
    """Test that config constants are properly defined."""
    assert isinstance(DEFAULT_TOP_K, int)
    assert DEFAULT_TOP_K > 0
    assert isinstance(EMBEDDING_MODEL, str)
    assert len(EMBEDDING_MODEL) > 0
    assert isinstance(CHUNK_SIZE, int)
    assert CHUNK_SIZE > 0
    assert isinstance(CHUNK_OVERLAP, int)
    assert CHUNK_OVERLAP >= 0
    assert CHUNK_OVERLAP < CHUNK_SIZE  # overlap should be less than chunk size


def test_search_returns_non_empty_strings():
    """Test that search results contain non-empty strings when results are found."""
    result = search("新潟")
    # Only check content if results are returned
    if result:
        assert all(len(r.strip()) > 0 for r in result)


def test_vectorstore_initialization():
    """Test that the vectorstore and related components can be imported without errors."""
    from src.rag_core import vectorstore, embeddings, docs

    # Basic checks to ensure components are initialized
    assert vectorstore is not None
    assert embeddings is not None
    assert docs is not None
    assert isinstance(docs, list)
