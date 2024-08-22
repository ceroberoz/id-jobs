# id-jobs: Your Gateway to Indonesian Job Opportunities! 🚀

Discover a treasure trove of curated job listings from trusted Indonesian sources, all neatly organized in an easy-to-use Google Sheets format. Whether you're a job seeker, recruiter, or just curious about the job market, id-jobs has got you covered!

🔗 Explore the latest job data: [https://s.id/id-jobs-v2](https://s.id/id-jobs-v2)

[![built with Codeium](https://codeium.com/badges/main)](https://codeium.com)
[![Run Scrapy Spiders](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml/badge.svg)](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml)

## What's id-jobs all about? 🤔

id-jobs is your friendly neighborhood job aggregator, bringing together exciting opportunities from various Indonesian companies and job portals. We use the power of Python and Scrapy to collect fresh job data regularly, so you're always in the know!

## Why you'll love id-jobs ❤️

- 🕒 Always up-to-date: Our job-hunting spiders work tirelessly to bring you the latest openings
- 🌈 Diverse opportunities: From tech giants to startups, we've got jobs for everyone
- 📊 Data at your fingertips: All neatly organized in Google Sheets for easy browsing and filtering

## Where do we find these awesome jobs? 🕵️‍♂️

We scour top companies and popular job portals, including:

- 🎥 Vidio
- 🛒 GoTo Group
- 🛍️ Blibli
- 👕 Evermos
- 🏥 SehatQ
- And many more! (Check out our full list in the source code)

## Getting Started (It's easier than you think!) 🚀

1. Clone this repository:
   ```
   git clone https://github.com/ceroberoz/id-jobs.git
   cd id-jobs
   ```

2. Set up your virtual environment (it's like a special playground for your project):
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the magic ingredients (dependencies):
   ```
   pip install -r requirements.txt
   playwright install
   ```

4. Run a job-hunting spider:
   ```
   scrapy crawl <crawler-name>
   ```
   Replace `<crawler-name>` with the specific crawler you want to run (e.g., `vidio`, `gotogroup`)

## Let's make it even more awesome! 🌟

Love the project? Have ideas? Contributions are super welcome! Feel free to submit pull requests to add new job sources or improve our existing crawlers.

## Connect and Visualize 📊

Want to take your job market analysis to the next level? The data from id-jobs can easily be connected to powerful visualization tools like Google Looker Studio or Tableau. Here's how:

1. Export the Google Sheets data to a CSV file.
2. Import the CSV into your preferred visualization tool.
3. Create stunning dashboards and insights about the Indonesian job market!

## Resources for the Curious Minds 📚

- [Scrapy Documentation](https://docs.scrapy.org/en/latest/intro/overview.html) - Learn the art of web scraping
- [Playwright Documentation](https://playwright.dev/docs/intro) - Master browser automation

## License

This project is licensed under the GNU General Public License v3 (GPL-3.0). Share the love and keep it open source! ❤️
