# id-jobs: Your One-Stop Shop for Indonesian Job Market Data

[![Scrape and Upload to Google Sheets](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml/badge.svg)](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.15+](https://img.shields.io/badge/python-3.15+-blue.svg)](https://www.python.org/downloads/)
![Made with Scrapy](https://img.shields.io/badge/Made%20with-Scrapy-green.svg)
![Made with Playwright](https://img.shields.io/badge/Made%20with-Playwright-orange.svg)

## Table of Contents
1. [Overview](#overview)
2. [Why id-jobs?](#why-id-jobs)
3. [How it Works](#how-it-works)
4. [Data Sources](#data-sources)
5. [Using the Data](#using-the-data)
6. [Features](#features)
7. [Quick Start Guide for Technical Users](#quick-start-guide-for-technical-users)
8. [Work in Progress](#work-in-progress)
9. [Contributing](#contributing)
10. [Support](#support)
11. [License](#license)

## Overview

📊 **View Job Data:** [https://s.id/id-jobs-v2](https://s.id/id-jobs-v2)

id-jobs is a tool that collects job listings from various Indonesian job boards and company websites, organizing them into one easy-to-access Google Sheet.

🇮🇩 **Important:** id-jobs is specifically designed for the Indonesian job market.

## Why id-jobs?

Finding the right job in Indonesia can be challenging, with information scattered across multiple websites. id-jobs simplifies this process by gathering job information from various Indonesian sources into one place, making it easier for job seekers to find opportunities.

## How it Works

id-jobs automatically visits Indonesian job websites, collects relevant information, and organizes it all in one spreadsheet. This process, called web scraping, is done respectfully and in line with each website's terms of service.

## Data Sources

We currently collect data from:
- Jobstreet Indonesia
- Glints Indonesia
- Kalibrr
- TopKarir
- Indeed Indonesia
- Various company career pages

## Using the Data

With all this Indonesian job data in one place, you can:
- Identify trends in job titles, salaries, or locations across Indonesia
- Create visual charts and graphs using tools like Google Looker Studio or Tableau
- Use spreadsheet functions to filter and analyze the Indonesian job market

## Features

- Automated daily data collection
- Centralized data storage in Google Sheets
- Easy-to-use interface for data analysis
- Support for multiple job boards and company websites
- Open-source codebase for community contributions

## Quick Start Guide for Technical Users

If you're interested in running the scrapers yourself or contributing to the project, we've prepared a detailed guide to help you get started quickly.

For step-by-step instructions on how to:
- Clone the project
- Set up your Python environment
- Install necessary tools
- Run the scrapers
- Explore and contribute to the project

Please refer to our [Quick Start Guide](QUICKSTART.md).

This guide provides beginner-friendly instructions for users on macOS, Linux, and Windows.

## Work in Progress

We're continuously updating our system to ensure we capture the most current job data. Some job sources might be temporarily unavailable as websites change, but we're working to keep the data flow consistent.

## Contributing

We welcome contributions from the community! Whether it's adding new features, fixing bugs, or improving documentation, your help is appreciated. Please see our [Contribution Guidelines](CONTRIBUTING.md) for more information.

## Support

If you encounter any issues or have questions, please:
1. Check our [FAQ](FAQ.md) for common questions and answers
2. Open an issue on our GitHub repository

## License

id-jobs is open source under the GPL-3.0 license. You're free to use, modify, and share the code, as long as you keep it open source too.

Remember: We always respect website terms of service when collecting data.
