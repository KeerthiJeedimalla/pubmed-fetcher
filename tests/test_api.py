from pubmed_fetcher.api import search_pubmed
import pytest

def test_search_pubmed_returns_list():
    """Test that search_pubmed returns a list of PMIDs"""
    results = search_pubmed("cancer", retmax=5)
    assert isinstance(results, list)
    assert len(results) <= 5

def test_empty_query():
    """Test handling of empty queries"""
    with pytest.raises(Exception):
        search_pubmed("")

# In api.py
def search_pubmed(query: str, retmax: int = 100) -> List[str]:
    if not query.strip():
        raise ValueError("Query cannot be empty")
    # Rest of your existing code        