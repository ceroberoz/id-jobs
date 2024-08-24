# Quick Start Guide for id-jobs

This guide provides instructions for setting up and running the id-jobs project locally. These steps are suitable for users familiar with command-line interfaces and basic programming concepts.

## Prerequisites

- Git
- Python 3.12+

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/ceroberoz/id-jobs.git
   cd id-jobs
   ```

2. Set up Python environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   playwright install
   ```

## Running Scrapers

1. Run a scraper (e.g., Jobstreet):
   ```
   scrapy crawl jobstreet
   ```

2. Save results to CSV:
   ```
   scrapy crawl jobstreet -o jobstreet_jobs.csv -t csv
   ```

## Project Structure

- `spiders/`: Individual scraper files
- `items.py`: Scraped data structure
- `pipelines.py`: Data processing and storage
- `settings.py`: Project configurations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes and push to your fork
4. Open a pull request with a clear description

## Updating

```
git pull origin main
pip install -r requirements.txt
```

## Troubleshooting

- Ensure Python 3.12+ is installed: `python --version`
- For issues, check GitHub issues or report a new one

## Responsible Scraping

- Respect `robots.txt` and terms of service
- Implement reasonable delays between requests
- Only collect publicly available data

For any additional questions or issues not covered here, please refer to the [README.md](README.md) or open an issue on the GitHub repository.
