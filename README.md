# id-jobs: Your One-Stop Shop for Indonesian Job Market Data

[![Scrape and Upload to Google Sheets](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml/badge.svg)](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
![Last Updated](https://img.shields.io/github/last-commit/ceroberoz/id-jobs)
![GitHub stars](https://img.shields.io/github/stars/ceroberoz/id-jobs?style=social)
![Made with Scrapy](https://img.shields.io/badge/Made%20with-Scrapy-green.svg)
![Made with Playwright](https://img.shields.io/badge/Made%20with-Playwright-orange.svg)

📊 **View Job Data:** [https://s.id/id-jobs-v2](https://s.id/id-jobs-v2)

id-jobs brings together job listings from various Indonesian job boards and company websites into one easy-to-access Google Sheet. We use open-source tools like Scrapy, Playwright, Pandas, and GitHub Actions to collect and organize this data daily.

🇮🇩 **Important:** id-jobs is specifically designed for the Indonesian job market.

## Why id-jobs?

Finding the perfect job in Indonesia can be overwhelming. Jumping between multiple websites, tracking different listings, and comparing salaries is time-consuming. id-jobs simplifies this process by gathering job information from various Indonesian sources into one place.

## How it Works

Think of id-jobs as your personal job-hunting assistant for the Indonesian market. It visits local job websites, collects relevant information, and organizes it all in one spreadsheet. This process, called web scraping, is done respectfully and in line with each website's terms of service.

We currently collect data from Indonesian job boards and company sites, including:
- Jobstreet Indonesia
- Glints Indonesia
- Kalibrr
- And more local sources!

## Making Sense of the Data

With all this Indonesian job data in one place, you can:
- Spot trends in job titles, salaries, or locations across Indonesia
- Create visual charts and graphs using tools like Google Looker Studio or Tableau
- Use spreadsheet functions to filter and analyze the Indonesian job market

## Get Involved (for Beginners)

Want to run the scrapers yourself or contribute to the project? Here's how to get started:

1. **Copy the project to your computer:**
   - Go to the [GitHub page](https://github.com/ceroberoz/id-jobs)
   - Click the green "Code" button and copy the URL
   - Open your computer's terminal
   - Type `git clone [paste URL here]` and press Enter

2. **Set up your workspace:**
   - Install Python from python.org
   - In the terminal, go to the project folder
   - Create a virtual environment: `python -m venv venv`
   - Activate it:
     - Windows: `venv\Scripts\activate`
     - Mac/Linux: `source venv/bin/activate`

3. **Install necessary tools:**
   - Run: `pip install -r requirements.txt`
   - Then: `playwright install`

4. **Run a scraper:**
   - To see results in the terminal:
     `scrapy crawl [scraper name]` (e.g., `scrapy crawl jobstreet`)
   - To save results to a file:
     `scrapy crawl [scraper name] -o filename.csv -t csv`

## Work in Progress

Some job sources might be temporarily unavailable as websites change. We're continuously updating our scrapers to keep the data flowing.

## License

id-jobs is open source under the GNU General Public License v3 (GPL-3.0). You're free to use, modify, and share the code, as long as you keep it open source too.

Remember: Always respect website terms of service when scraping!
