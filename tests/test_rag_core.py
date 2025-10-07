import os
import sys
import pytest

# ensure project root is on sys.path
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from rag_core import search, TOP_K


def test_search_returns_list_and_max_top_k():
    """Smoke test: search() returns a list of strings with length <= TOP_K."""
    # use a simple prompt; behavior depends on data in docs/
    result = search("テスト")
    assert isinstance(result, list)
    assert all(isinstance(r, str) for r in result)
    assert len(result) <= TOP_K
