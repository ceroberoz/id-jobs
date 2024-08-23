[![Scrape and Upload to Google Sheets](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml/badge.svg)](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
![Last Updated](https://img.shields.io/github/last-commit/ceroberoz/id-jobs)
![GitHub stars](https://img.shields.io/github/stars/ceroberoz/id-jobs?style=social)
![Made with Scrapy](https://img.shields.io/badge/Made%20with-Scrapy-green.svg)
![Made with Playwright](https://img.shields.io/badge/Made%20with-Playwright-orange.svg)

📊 **Google Sheets Output:** [https://s.id/id-jobs-v2](https://s.id/id-jobs-v2)
🐙 **GitHub Repository:** [https://github.com/ceroberoz/id-jobs](https://github.com/ceroberoz/id-jobs)

id-jobs is a project that collects and organizes job listings from various Indonesian job boards and company websites. It's built with the help of open-source tools like Scrapy, Playwright, Pandas, GitHub Actions, and Google Sheets API. The development process is enhanced by using Zed as a text editor with Claude 3.5 Sonnet assistance.

## The Job Search Struggle

Have you ever felt overwhelmed trying to find the perfect job? Scouring multiple websites, keeping track of different listings, and trying to compare salaries can be exhausting. id-jobs aims to solve this problem by bringing together job listings from various sources into one easy-to-access place.

## How id-jobs Works

id-jobs uses web scraping technology to collect job information from different websites. Web scraping is like having a robot assistant that visits websites and collects specific information for you. It's generally legal as long as it respects the website's terms of service and doesn't overload their servers.

Our scrapers collect data from popular job boards and company career pages, including:
- Jobstreet
- Glints
- Kalibrr
- And many more!

## Analyzing the Data

Once the job data is collected, you can use it to gain insights into the job market. You can import the data into tools like Google Looker Studio, Metabase, or Tableau to create visualizations and dashboards. Even simple spreadsheet functions like pivot tables can help you analyze trends in job titles, salaries, or locations.

## Getting Started (for Beginners)

1. **Clone the repository:**
   - Click the green "Code" button on this page
   - Copy the URL
   - Open your terminal or command prompt
   - Type `git clone [paste URL here]` and press Enter

2. **Set up your environment:**
   - Install Python from python.org if you haven't already
   - In your terminal, navigate to the project folder
   - Create a virtual environment: `python -m venv venv`
   - Activate it:
     - Windows: `venv\Scripts\activate`
     - Mac/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   - Run: `pip install -r requirements.txt`
   - Then: `playwright install`

4. **Run a scraper:**
   - To run a scraper and see the output in the terminal:
     Type: `scrapy crawl [scraper name]` (e.g., `scrapy crawl jobstreet`)
   - To generate a local CSV file with the scraped data:
     Type: `scrapy crawl [scraper name] -o filename.csv -t csv`
     (Replace `filename` with your desired name, e.g., `jobstreet_data.csv`)

## Work in Progress

Please note that some job sources might be temporarily unavailable due to website changes. We're working on updating these as quickly as possible.

## License

This project is licensed under the GNU General Public License v3 (GPL-3.0). This means you're free to use, modify, and distribute the code, as long as you keep it open source.

(Side note: While web scraping is generally accepted, always make sure to review and respect each website's terms of service.)
