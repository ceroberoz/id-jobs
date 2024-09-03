# id-jobs: Your One-Stop Shop for Indonesian Job Market Data

[![Daily update to Google Sheets](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml/badge.svg)](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
![Made with Scrapy](https://img.shields.io/badge/Made%20with-Scrapy-green.svg)
![Made with Playwright](https://img.shields.io/badge/Made%20with-Playwright-orange.svg)

## What's New?

- **Work Arrangement Feature**: Track whether jobs are Remote, Hybrid, or On-site.
- **Job Apply End Date**: Automatically calculate application deadlines (30 days from last seen date).
- **Enhanced Data Cleaning**: Improved pre-upload data sanitization process.
- **Job Age Feature**: Track the age of job listings to identify the most recent opportunities.
- **Expanded Job Portal Coverage**: Added new job portals including Blibli, Dealls, Evermos, GoTo, and Vidio.

## Overview

id-jobs uses advanced web scraping techniques to gather job listings from various Indonesian job portals and company websites, respecting each website's terms of service.

📊 **View Job Data:** [https://s.id/id-jobs-v2](https://s.id/id-jobs-v2)

🇮🇩 **Note:** id-jobs is specifically designed for the Indonesian job market.

## Job Age Color Guidelines

To help users quickly identify the freshness of job listings, we use a color-coded system based on the job's age:

| Job Age Category | Time Range | Color | Description |
|------------------|------------|-------|-------------|
| New | <= 1 day | ![#B3E6B3](https://via.placeholder.com/15/B3E6B3/000000?text=+) Bright Light Green | Most recent and attractive opportunities |
| Hot | 1 to 7 days | ![#FFCC66](https://via.placeholder.com/15/FFCC66/000000?text=+) Warm Light Orange | Very recent and appealing listings |
| Recent | 8 to 15 days | ![#99CCFF](https://via.placeholder.com/15/99CCFF/000000?text=+) Light Blue | Still fresh and noteworthy opportunities |
| Aging | 16 to 21 days | ![#F2F2F2](https://via.placeholder.com/15/F2F2F2/000000?text=+) Very Light Gray | Older listings, less priority |
| Old | 22 to 30 days | ![#E6E6E6](https://via.placeholder.com/15/E6E6E6/000000?text=+) Light Gray | Significantly older listings, low priority |
| Expired | > 30 days | ![#D9D9D9](https://via.placeholder.com/15/D9D9D9/000000?text=+) Medium Gray | Outdated listings, likely no longer active |

This color scheme is designed to guide users towards the most recent job opportunities while de-emphasizing older listings.

## How It Works

id-jobs automatically visits Indonesian job websites, collects relevant information, and organizes it in a single spreadsheet. The data is cleaned and formatted before being uploaded to ensure consistency and readability.

![How Scraper Works](how-scraper-works.gif)

## Preview

Here's a preview of the id-jobs data in action:

![id-jobs Preview](screen-capture-dev.png)

## Why Use id-jobs?

Finding the right job in Indonesia can be challenging. id-jobs simplifies this process by consolidating information from multiple websites into one place, providing additional insights such as work arrangements and application deadlines.

## Data Sources

We collect data from a wide range of sources, including:
- Jobstreet
- Glints
- Kalibrr
- TopKarir
- Indeed
- Blibli
- Dealls
- Evermos
- GoTo
- Vidio
- Various company career pages

## Features

- **Daily Updates**: Automated daily updates through CI/CD pipelines.
- **Work Arrangement Tracking**: Identify Remote, Hybrid, and On-site opportunities.
- **Application Deadline Estimation**: Calculated end dates for job applications.
- **Optimized Data Collection**: Improved accuracy and coverage of job listings.
- **User-Friendly Interface**: Access job data through a Google Sheets interface.
- **Comprehensive Information**: Data from multiple job boards and company websites.
- **Job Age Tracking**: Identify the most recent job listings.

## Getting Started

For a quick guide on how to use id-jobs, refer to our [Quickstart Guide](QUICKSTART.md).

## FAQ

Have questions? Check out our [FAQ](FAQ.md) for answers to common queries.

## Legal

id-jobs is open source under the GPL-3.0 license. You're free to use, modify, and share the code, as long as you keep it open source too.

We always respect website terms of service when collecting data.