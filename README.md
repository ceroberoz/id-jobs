# id-jobs: Your Treasure Map to Indonesian Job Opportunities! 🗺️💼

Ahoy, job seekers and data enthusiasts! Welcome to id-jobs, your ultimate adventure guide to the exciting world of Indonesian employment. We've scoured the digital seas to bring you a treasure trove of job listings, all neatly charted in a user-friendly Google Sheets map. Whether you're hunting for your dream job, recruiting top talent, or just curious about the job market landscape, id-jobs is your trusty compass!

🔗 Set sail for job data: [https://s.id/id-jobs-v2](https://s.id/id-jobs-v2)

[![built with Codeium](https://codeium.com/badges/main)](https://codeium.com)
[![Run Scrapy Spiders](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml/badge.svg)](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml)

## What's the id-jobs treasure all about? 🏴‍☠️

id-jobs is your friendly neighborhood job data pirate (the good kind!), sailing the vast internet seas to gather shiny job opportunities from various Indonesian islands (companies) and ports (job portals). We use the mystical powers of Python and Scrapy to continuously update our treasure map, ensuring you always have the freshest leads!

## Why you'll fall in love with id-jobs ❤️

- 🕒 Always on the horizon: Our tireless job-hunting spiders keep your treasure map up-to-date
- 🌈 A rainbow of opportunities: From tech unicorns to hidden startup gems, we've got a chest full of diverse jobs
- 📊 X marks the spot: All job treasures are neatly organized in Google Sheets for easy digging

## Our favorite hunting grounds 🏝️

We explore far and wide, including:

- 🎥 Vidio Island
- 🛒 GoTo Archipelago
- 🛍️ Blibli Bay
- 👕 Evermos Cove
- And many more uncharted territories! (Check our maps in the source code)

## Join the crew (It's a piece of cake, matey!) 🏴‍☠️

1. Clone the treasure map:
   ```
   git clone https://github.com/ceroberoz/id-jobs.git
   cd id-jobs
   ```

2. Create your secret hideout (virtual environment):
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Gather your pirate tools (install dependencies):
   ```
   pip install -r requirements.txt
   playwright install
   ```

4. Set sail with a job-hunting spider:
   ```
   scrapy crawl <crawler-name>
   ```
   Replace `<crawler-name>` with your chosen adventure (e.g., `vidio`, `gotogroup`)

## Chart your own course! 🧭

New to coding? No worries! This project is perfect for beginners looking to dip their toes into web scraping and data analysis. Start by exploring the code, run a few spiders, and before you know it, you'll be a data pirate pro!

## Create your own treasure maps 🗺️

Want to turn your job data into dazzling visuals? Here's how to connect id-jobs to powerful tools like Google Looker Studio or Tableau:

1. Download your Google Sheets treasure map as a CSV file.
2. Import this CSV booty into your favorite visualization tool.
3. Craft stunning dashboards to reveal insights about the Indonesian job market!

## Expand your pirate knowledge 📚

- [Scrapy Documentation](https://docs.scrapy.org/en/latest/intro/overview.html) - Master the art of web scraping
- [Playwright Documentation](https://playwright.dev/docs/intro) - Become a browser automation wizard

## The Pirate Code (License)

This treasure is shared under the GNU General Public License v3 (GPL-3.0). Share the wealth and keep the high seas of open source free! ❤️
