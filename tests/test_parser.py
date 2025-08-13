from pubmed_fetcher.parser import parse_pubmed_xml
import pytest

SAMPLE_XML = """
<PubmedArticleSet>
  <PubmedArticle>
    <PMID>12345</PMID>
    <Article>
      <ArticleTitle>Test Cancer Study</ArticleTitle>
      <Journal>
        <JournalIssue>
          <PubDate>
            <Year>2023</Year>
            <Month>Jun</Month>
          </PubDate>
        </JournalIssue>
      </Journal>
      <AuthorList>
        <Author>
          <LastName>Smith</LastName>
          <ForeName>John</ForeName>
          <AffiliationInfo>
            <Affiliation>Harvard University</Affiliation>
          </AffiliationInfo>
        </Author>
        <Author>
          <LastName>Doe</LastName>
          <ForeName>Jane</ForeName>
          <AffiliationInfo>
            <Affiliation>Pfizer Inc</Affiliation>
          </AffiliationInfo>
        </Author>
      </AuthorList>
    </Article>
  </PubmedArticle>
</PubmedArticleSet>"""

def test_parse_pubmed_xml_structure():
    """Test XML parsing extracts correct fields"""
    articles = parse_pubmed_xml(SAMPLE_XML)
    
    # Test basic fields
    assert len(articles) == 1
    article = articles[0]
    assert article['pmid'] == '12345'
    assert article['title'] == 'Test Cancer Study'
    assert article['date'] == "2023-Jun"
    
    # Test authors and affiliations
    assert len(article['authors']) == 2
    assert ("John Smith", "Harvard University") in article['authors']
    assert ("Jane Doe", "Pfizer Inc") in article['authors']
    assert "Harvard University" in article['affiliations']
    assert "Pfizer Inc" in article['affiliations']

def test_parse_incomplete_xml():
    """Test parsing with missing fields"""
    incomplete_xml = """
    <PubmedArticleSet>
      <PubmedArticle>
        <PMID>67890</PMID>
        <Article>
          <ArticleTitle>Incomplete Study</ArticleTitle>
        </Article>
      </PubmedArticle>
    </PubmedArticleSet>"""
    
    articles = parse_pubmed_xml(incomplete_xml)
    assert articles[0]['pmid'] == '67890'
    assert articles[0]['title'] == 'Incomplete Study'
    assert articles[0]['date'] == "Unknown"
    assert articles[0]['authors'] == []
    assert articles[0]['affiliations'] == []