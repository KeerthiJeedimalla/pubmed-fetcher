from pubmed_fetcher.filter import filter_industry_affiliations

def test_filter_industry_affiliations():
    """Test filtering of industry affiliations"""
    test_articles = [
        {
            'pmid': '1',
            'affiliations': ['Pfizer Inc', 'Harvard University']
        },
        {
            'pmid': '2', 
            'affiliations': ['MIT']
        }
    ]
    
    filtered = filter_industry_affiliations(test_articles)
    assert len(filtered) == 1
    assert filtered[0]['pmid'] == '1'
    assert filtered[0]['affiliations'] == ['Pfizer Inc']