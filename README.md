# id-jobs: Your Gateway to Indonesian Job Market Data! 🚀💼

Hey there, job seekers, recruiters, and data enthusiasts! Welcome to id-jobs 2.0, your ultimate tool for exploring the exciting world of Indonesian employment. We've aggregated job listings from top companies and portals, all neatly organized in a user-friendly Google Sheet. Whether you're hunting for your dream job, recruiting top talent, or just curious about the job market landscape, id-jobs is your go-to resource!

🔗 Access the latest job data: [https://s.id/id-jobs-v2](https://s.id/id-jobs-v2)

[![built with Codeium](https://codeium.com/badges/main)](https://codeium.com)
[![Run Scrapy Spiders](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml/badge.svg)](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml)

## What's id-jobs all about? 🔍

id-jobs is an open-source project that aggregates job listings from top Indonesian companies and job portals, all in one easy-to-use Google Sheet! We use Python and Scrapy to continuously update our data, ensuring you always have the most current information.

## Why you'll love id-jobs ❤️

- 🕒 Always fresh: Our sheets are updated DAILY at 00:00 UTC
- 🌈 Comprehensive data: We've added even more job sources in version 2.0
- 📊 Improved accuracy: Our data is more reliable than ever
- 👩‍💻 Beginner-friendly: Perfect for those starting their coding journey

## Important Note ⚠️

Some spiders might not be working due to recent changes in the source websites. As a result, some data might not be showing up on the Google Sheet. We're working on repairing these issues as quickly as possible. Thanks for your patience and understanding!

## Who is id-jobs for? 👥

- Job seekers looking for roles that match their skills, location, and salary expectations
- Recruiters seeking to understand the Indonesian job market
- Data enthusiasts interested in analyzing employment trends
- Coding newbies wanting to practice web scraping and data analysis

## Get started in 4 easy steps! 🚀

1. Clone the repo:
   ```
   git clone https://github.com/ceroberoz/id-jobs.git
   cd id-jobs
   ```

2. Set up your environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   playwright install
   ```

4. Run your first job crawler:
   ```
   scrapy crawl <crawler-name>
   ```
   Replace `<crawler-name>` with your chosen crawler (e.g., `vidio`, `gotogroup`)

## Visualize your data 📊

Want to create stunning visualizations with the job data? Here's how:

1. Download the Google Sheet as a CSV file.
2. Import this CSV into tools like Google Looker Studio or Tableau.
3. Create insightful dashboards to reveal trends in the Indonesian job market!

## Learn more 📚

- [Scrapy Documentation](https://docs.scrapy.org/en/latest/intro/overview.html) - Master web scraping
- [Playwright Documentation](https://playwright.dev/docs/intro) - Become a browser automation pro

## Important note 🇮🇩

id-jobs is specifically tailored for the Indonesian job market. It's our way of addressing the unique challenges and opportunities in our local job scene!

## License

This project is shared under the GNU General Public License v3 (GPL-3.0). Let's democratize job market data together! ❤️

If you're excited about this project, don't forget to fork, star, and share!

#OpenSource #DataScience #JobMarket #Indonesia #CodingForBeginners #GitHub
