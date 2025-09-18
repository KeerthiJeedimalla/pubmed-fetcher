# PubMed Industry Affiliation Fetcher



A Python tool to identify research papers with pharmaceutical/biotech industry affiliations from PubMed.

## Features
- PubMed API integration
- Industry affiliation detection
- CSV output with PMIDs, titles, dates, and affiliations
- CLI interface with query options

## Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/pubmed-fetcher.git
cd pubmed-fetcher

# Install dependencies
poetry install
```

## Usage
```bash
# Basic query (console output)
poetry run python -m pubmed_fetcher.cli "cancer treatment"

# Save to CSV
poetry run python -m pubmed_fetcher.cli "mRNA vaccine" --output results.csv
```

## Example Output CSV
| pmid     | title                          | date    | affiliations               |
|----------|--------------------------------|---------|----------------------------|
| 12345678 | Novel Cancer Drug Study        | 2023-Jun| Pfizer Inc, Genentech      |

## Configuration
Edit `filter.py` to add more industry keywords:
```python
INDUSTRY_KEYWORDS = {
    'pharma', 'biotech', 'inc', 'ltd',
    # Add more keywords here
}
```

## License
MIT - See for details.
