from typing import List, Dict

# Keywords to identify industry affiliations
INDUSTRY_KEYWORDS = {
    'pharma', 'biotech', 'pharmaceutical', 'inc', 'ltd',
    'corporation', 'company', 'research and development',
    'rltd', 'plc', 'co.', 'genentech', 'novartis', 'pfizer'
}

def filter_industry_affiliations(articles: List[Dict]) -> List[Dict]:
    """Filter papers with industry affiliations"""
    filtered = []
    
    for article in articles:
        industry_affiliations = [
            aff for aff in article['affiliations']
            if any(keyword in aff.lower() in aff.lower()
                  for keyword in INDUSTRY_KEYWORDS)
        ]
        
        if industry_affiliations:
            filtered.append({
                'pmid': article['pmid'],
                'title': article['title'],
                'date': article['date'],
                'affiliations': industry_affiliations
            })
    
    return filtered