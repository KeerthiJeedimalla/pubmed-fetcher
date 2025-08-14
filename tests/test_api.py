import requests
from typing import List  # Add this import
from pubmed_fetcher.api import search_pubmed
import pytest

def test_search_pubmed_returns_list():
    """Test that search_pubmed returns a list of PMIDs"""
    results = search_pubmed("cancer", retmax=5)
    assert isinstance(results, list)
    assert len(results) <= 5

def test_empty_query():
    """Test handling of empty queries"""
    with pytest.raises(ValueError):
        search_pubmed("")

# In api.py
def search_pubmed(query: str, retmax: int = 100) -> list[str]:
    """Fetch PubMed article IDs (PMIDs) for a query"""
    if not query.strip():  # Check for empty/whitespace-only queries
        raise ValueError("Query cannot be empty")
    
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }
    
    try:
        response = requests.get(f"{base_url}esearch.fcgi", params=params)
        response.raise_for_status()
        return response.json().get("esearchresult", {}).get("idlist", [])
    except Exception as e:
        print(f"API Error: {e}")
        return []  # Return empty list on network/API errors