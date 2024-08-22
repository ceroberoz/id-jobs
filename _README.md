# id-jobs: Indonesia Job Information Aggregator

Explore curated job listings from trusted Indonesian sources, conveniently presented in Google Sheets format.

View the latest job data: [https://s.id/id-jobs](https://s.id/id-jobs)

[![built with Codeium](https://codeium.com/badges/main)](https://codeium.com)
[![Run Scrapy Spiders](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml/badge.svg)](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml)

## About

id-jobs is a Python-based project that aggregates job listings from various Indonesian companies and job portals. It uses Scrapy for web scraping and automates data collection through GitHub Actions.

## Features

- Aggregates job data from multiple sources
- Regularly updated through automated scraping
- Data presented in an easy-to-use Google Sheets format

## Supported Job Sources

### Companies
- Vidio
- GoTo Group
- Blibli
- Evermos
- SehatQ

### Job Portals
- Kalibrr
- Dealls
- Jobstreet

(See full list in the source code)

## Getting Started

1. Clone this repository:
   ```
   git clone https://github.com/ceroberoz/id-jobs.git
   cd id-jobs
   ```

2. Set up a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   playwright install
   ```

4. Run a specific crawler:
   ```
   scrapy crawl <crawler-name>
   ```

Replace `<crawler-name>` with the name of the specific crawler you want to run (e.g., `vidio`, `gotogroup`, etc.)

## Contributing

Contributions are welcome! Feel free to submit pull requests to add new job sources or improve existing crawlers.

## Resources

- [Scrapy Documentation](https://docs.scrapy.org/en/latest/intro/overview.html)
- [Playwright Documentation](https://playwright.dev/docs/intro)

## License

GNU General Public License v3 (GPL-3.0)
