# Quick Start Guide for id-jobs

This guide provides detailed instructions for setting up and running the id-jobs project on your local machine. These steps are suitable for beginners and cover macOS, Linux, and Windows operating systems.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Step 1: Clone the Project](#step-1-clone-the-project)
3. [Step 2: Set Up Python Environment](#step-2-set-up-python-environment)
4. [Step 3: Install Necessary Tools](#step-3-install-necessary-tools)
5. [Step 4: Run the Scrapers](#step-4-run-the-scrapers)
6. [Step 5: Explore and Contribute](#step-5-explore-and-contribute)
7. [Project Structure](#project-structure)
8. [Updating the Project](#updating-the-project)
9. [Troubleshooting](#troubleshooting)
10. [Common Issues and Solutions](#common-issues-and-solutions)
11. [Responsible Scraping](#responsible-scraping)

## Prerequisites

- Git
- Python 3.15 or higher

## Step 1: Clone the Project

1. Install Git from [git-scm.com](https://git-scm.com/downloads) if you haven't already.
2. Open your terminal (Command Prompt on Windows, Terminal on macOS/Linux).
3. Navigate to where you want to store the project:
   ```
   cd path/to/your/preferred/directory
   ```
4. Clone the repository:
   ```
   git clone https://github.com/ceroberoz/id-jobs.git
   ```
5. Move into the project directory:
   ```
   cd id-jobs
   ```

## Step 2: Set Up Python Environment

1. Install Python 3.15 or higher from [python.org](https://www.python.org/downloads/).
2. Create a virtual environment:
   - On Windows:
     ```
     python -m venv venv
     ```
   - On macOS/Linux:
     ```
     python3 -m venv venv
     ```
3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

## Step 3: Install Necessary Tools

1. Upgrade pip (Python's package installer):
   ```
   pip install --upgrade pip
   ```
2. Install project dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```
   playwright install
   ```

## Step 4: Run the Scrapers

1. To see results in the terminal:
   ```
   scrapy crawl jobstreet
   ```
2. To save results to a CSV file:
   ```
   scrapy crawl jobstreet -o jobstreet_jobs.csv -t csv
   ```

Replace `jobstreet` with other scraper names to collect data from different sources.

## Step 5: Explore and Contribute

- Check the `spiders` folder to see all available scrapers.
- To modify a scraper, open its file (e.g., `jobstreet.py`) in a text editor.
- If you make improvements, consider contributing back to the project:
  1. Fork the repository on GitHub
  2. Create a new branch for your feature
  3. Commit your changes and push to your fork
  4. Open a pull request with a clear description of your changes

## Project Structure

Here's an overview of the main directories and files in the project:

- `spiders/`: Contains individual scraper files for each job board
- `items.py`: Defines the structure of scraped data
- `pipelines.py`: Handles data processing and storage
- `settings.py`: Contains project settings and configurations

## Updating the Project

To update your local copy of the project:

1. Ensure you're in the project directory
2. Pull the latest changes:
   ```
   git pull origin main
   ```
3. Update dependencies:
   ```
   pip install -r requirements.txt
   ```

## Troubleshooting

- If you encounter any issues, first ensure your Python version is 3.15 or higher:
  ```
  python --version
  ```
- For macOS/Linux users, you might need to use `python3` instead of `python` in commands.
- If a website structure changes, the scraper might stop working. Check the project's issues on GitHub or report a new one.

## Common Issues and Solutions

1. **Scraper not working for a specific website**
   - Check if the website structure has changed
   - Verify your internet connection
   - Ensure you're using the latest version of the scraper

2. **Import errors when running scrapers**
   - Make sure you've activated the virtual environment
   - Verify all dependencies are installed correctly

3. **Permission issues (especially on Linux/macOS)**
   - Ensure you have the necessary permissions to write to the output directory
   - Try running the command with `sudo` (use with caution)

## Responsible Scraping

Remember to always scrape responsibly:
- Respect each website's `robots.txt` file and terms of service.
- Implement reasonable delays between requests to avoid overloading servers.
- Only collect publicly available data that you have permission to access.

For any questions or issues not covered here, please open an issue on the GitHub repository.
