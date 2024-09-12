# id-jobs: Indonesian Job Market Data Aggregator 💼🇮🇩

[![Daily Job Data Update](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml/badge.svg)](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
![Powered by Scrapy](https://img.shields.io/badge/Powered%20by-Scrapy-green.svg)
![Enhanced by Playwright](https://img.shields.io/badge/Enhanced%20by-Playwright-orange.svg)

## 🆕 Latest Updates

- Added Koltiva job listings
- Improved Karir.com data collection
- Enhanced data cleaning for job titles and types
- Added work arrangement and job level detection
- Improved error handling

## 📊 Overview

id-jobs collects job listings from Indonesian job portals and company websites, respecting each site's terms of service.

**View the Data:** [https://s.id/id-jobs-v2](https://s.id/id-jobs-v2)

## 🎨 Job Age Colors

| Age | Time | Color |
|-----|------|-------|
| New | ≤ 1 day | ![#00CC00](https://via.placeholder.com/15/00CC00/000000?text=+) Bright Green |
| Hot | 1-7 days | ![#FF6600](https://via.placeholder.com/15/FF6600/000000?text=+) Bright Orange |
| Recent | 8-15 days | ![#FFFF00](https://via.placeholder.com/15/FFFF00/000000?text=+) Bright Yellow |
| Aging | 16-21 days | ![#E6E6E6](https://via.placeholder.com/15/E6E6E6/000000?text=+) Light Gray |
| Old | 22-30 days | ![#CCCCCC](https://via.placeholder.com/15/CCCCCC/000000?text=+) Medium Gray |
| Expired | > 30 days | ![#B3B3B3](https://via.placeholder.com/15/B3B3B3/000000?text=+) Dark Gray |
## 🔧 How It Works

id-jobs automatically collects job data from various websites, cleans the information, and compiles it into a single spreadsheet.

![Scraping Process](how-scraper-works.gif)

## 👀 Preview

![id-jobs Preview](screen-capture-dev.png)

## 🌟 Why Use id-jobs?

id-jobs simplifies job searching by gathering information from multiple sources into one place, providing insights on work arrangements, job levels, and application deadlines.

## 📚 Data Sources

We collect data from various job portals and company websites, including:
Blibli, Dealls, Evermos, Flip, GoTo, Jobstreet, Kalibrr, Karir.com, Kredivo, SoftwareOne, Tiket, and more.

## 🚀 Features

- Daily updates
- Work arrangement identification
- Job level detection
- Application deadline calculation
- Improved data accuracy
- User-friendly Google Sheets interface
- Job age tracking

## 🏁 Getting Started

For a quick guide, see our [Quickstart Guide](QUICKSTART.md).

## ❓ FAQ

Check our [FAQ](FAQ.md) for common questions.

## 📄 License

id-jobs is open source under the GPL-3.0 license. You can use, modify, and share the code, as long as you keep it open source.

We respect website terms of service when collecting data.
