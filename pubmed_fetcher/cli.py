import click
import logging
import csv
from pathlib import Path
from .api import search_pubmed, fetch_article_details
from .parser import parse_pubmed_xml
from .filter import filter_industry_affiliations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.argument('query')
@click.option('--output', '-o', default=None, help='Output CSV file')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed logs')
def main(query: str, output: str, verbose: bool):
    """Fetch papers with industry affiliations"""
    if verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.info(f"Starting search for: {query}")
    
    try:
        # 1. Search PubMed
        pmids = search_pubmed(query, retmax=50)
        logger.info(f"Found {len(pmids)} potential articles")
        
        if not pmids:
            logger.error("No articles found for query")
            return
        
        # 2. Fetch details
        logger.debug("Fetching article details...")
        xml_data = fetch_article_details(pmids)
        
        # 3. Parse and filter
        logger.debug("Parsing XML...")
        articles = parse_pubmed_xml(xml_data)
        filtered = filter_industry_affiliations(articles)
        logger.info(f"Found {len(filtered)} articles with industry affiliations")
        
        # 4. Output results
        if output:
            output_path = Path(output)
            output_path.write_text("")  # Clear existing file
            with open(output, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['pmid', 'title', 'date', 'affiliations'])
                writer.writeheader()
                writer.writerows(filtered)
            logger.info(f"Results saved to {output_path.absolute()}")
        else:
            click.echo("\nResults:")
            for article in filtered:
                click.echo(f"\nPMID: {article['pmid']}")
                click.echo(f"Title: {article['title']}")
                click.echo(f"Date: {article['date']}")
                click.echo("Affiliations:")
                for aff in article['affiliations']:
                    click.echo(f"- {aff}")
                    
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=verbose)
        raise click.Abort()

if __name__ == "__main__":
    main()