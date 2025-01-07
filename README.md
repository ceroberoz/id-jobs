# id-jobs: Indonesian Job Market Data Aggregator 💼🇮🇩

[![Daily Job Data Update](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml/badge.svg)](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml)  
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)  
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)  
![Powered by Scrapy](https://img.shields.io/badge/Powered%20by-Scrapy-green.svg)  
![Enhanced by Playwright](https://img.shields.io/badge/Enhanced%20by-Playwright-orange.svg)

## 🆕 Latest Updates

- Added **TechInAsia** spider for job data collection
- Integrated **Algolia API** for efficient data retrieval
- Improved data sanitization and CSV export
- Enhanced error handling and logging
- Updated docs with new data source details

## 📊 Overview

id-jobs gathers job listings from Indonesian job portals and company websites, following each site's terms of service.

**View Data on Google Sheets:** [https://s.id/id-jobs-v2](https://s.id/id-jobs-v2)  
**View Dashboard on Looker Studio:** [https://s.id/id-jobs-dashboard](https://s.id/id-jobs-dashboard)

## 🎨 Job Age Colors

| Age        | Time       | Color          |
|------------|------------|----------------|
| New        | ≤ 1 day    | ![#00CC00](https://via.placeholder.com/15/00CC00/000000?text=+) Green |
| Hot        | 1-7 days   | ![#FF6600](https://via.placeholder.com/15/FF6600/000000?text=+) Orange |
| Recent     | 8-15 days  | ![#FFFF00](https://via.placeholder.com/15/FFFF00/000000?text=+) Yellow |
| Aging      | 16-21 days | ![#E6E6E6](https://via.placeholder.com/15/E6E6E6/000000?text=+) Gray |
| Old        | 22-30 days | ![#CCCCCC](https://via.placeholder.com/15/CCCCCC/000000?text=+) Dark Gray |
| Expired    | > 30 days  | ![#B3B3B3](https://via.placeholder.com/15/B3B3B3/000000?text=+) Very Dark Gray |

## 🔧 How It Works

id-jobs scrapes job data from multiple sites, cleans it, and compiles it into a single spreadsheet. We use **Scrapy** for most sites and **Playwright** for JavaScript-heavy sites.

![Scraping Process](how-scraper-works.gif)

## 👀 Preview

![id-jobs Preview](screen-capture-dev.png)

## 🌟 Why Use id-jobs?

id-jobs aggregates job listings in one place, offering insights like work arrangements, job levels, and deadlines.

## 📚 Data Sources

We collect data from several job portals and company websites, including:  
Blibli, Dealls, Evermos, Flip, GoTo, Glints (Lite), Jobstreet, Kalibrr, Karir.com, Kredivo, Mekari, SoftwareOne, Tiket, Tech in Asia Jobs, and more.

## 🚀 Features

- Daily updates
- Identifies work arrangements & job levels
- Tracks application deadlines
- Accurate data
- User-friendly Google Sheets interface
- Tracks job age
- Handles JavaScript-rendered content
- Efficient pagination
- Integrated with Algolia API

## 🏁 Getting Started

For a quick guide, check the [Quickstart Guide](QUICKSTART.md).

## ❓ FAQ

See our [FAQ](FAQ.md) for common questions.

## 📄 License

id-jobs is open source under the GPL-3.0 license. You can use, modify, and share it, as long as it remains open source.  
We respect website terms of service when collecting data.
