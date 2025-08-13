import requests
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

def search_pubmed(query: str, retmax: int = 100) -> List[str]:
    """Fetch PubMed article IDs (PMIDs) for a query"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }
    response = requests.get(f"{base_url}esearch.fcgi", params=params)
    response.raise_for_status()
    return response.json().get("esearchresult", {}).get("idlist", [])

def fetch_article_details(pmids: List[str]) -> str:
    """Fetch full article data in XML format"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }
    response = requests.get(f"{base_url}efetch.fcgi", params=params)
    response.raise_for_status()
    return response.text