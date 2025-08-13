from bs4 import BeautifulSoup
from typing import List, Dict

def parse_pubmed_xml(xml_content: str) -> List[Dict]:
    """
    Parse PubMed XML into structured data
    
    Args:
        xml_content: Raw XML string from PubMed API
        
    Returns:
        List of dictionaries containing:
        - pmid (str)
        - title (str)
        - date (str)
        - authors (list of tuples: (name, affiliation))
        - affiliations (list of str)
    """
    soup = BeautifulSoup(xml_content, 'lxml-xml')
    articles = []
    
    for article in soup.find_all('PubmedArticle'):
        try:
            # Extract basic information
            pmid = article.find('PMID').text if article.find('PMID') else 'N/A'
            title = article.find('ArticleTitle').text if article.find('ArticleTitle') else 'Untitled'
            
            # Extract authors and affiliations
            authors = []
            affiliations = set()
            for author in article.find_all('Author'):
                last_name = author.find('LastName')
                fore_name = author.find('ForeName')
                if last_name and fore_name:
                    name = f"{fore_name.text} {last_name.text}"
                    aff = author.find('AffiliationInfo')
                    if aff and aff.Affiliation:
                        aff_text = aff.Affiliation.text.strip()
                        authors.append((name, aff_text))
                        affiliations.add(aff_text)
            
            # Robust date extraction
            pub_date = article.find('PubDate')
            date_parts = []
            if pub_date:
                for part in ['Year', 'Month', 'Day']:
                    elem = pub_date.find(part)
                    if elem and elem.text:
                        date_parts.append(elem.text)
            date = "-".join(date_parts) if date_parts else "Unknown"
            
            articles.append({
                'pmid': pmid,
                'title': title,
                'date': date,
                'authors': authors,
                'affiliations': list(affiliations)
            })
            
        except Exception as e:
            print(f"Error parsing article: {e}")
            continue
            
    return articles