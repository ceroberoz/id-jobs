# id-jobs: Your One-Stop Shop for Indonesian Job Market Data (Now with 50% Less Frustration!)

[![Scrape and Upload to Google Sheets](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml/badge.svg)](https://github.com/ceroberoz/id-jobs/actions/workflows/scrape.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.15+](https://img.shields.io/badge/python-3.15+-blue.svg)](https://www.python.org/downloads/)
![Last Updated](https://img.shields.io/github/last-commit/ceroberoz/id-jobs)
![Made with Scrapy](https://img.shields.io/badge/Made%20with-Scrapy-green.svg)
![Made with Playwright](https://img.shields.io/badge/Made%20with-Playwright-orange.svg)

📊 **View Job Data:** [https://s.id/id-jobs-v2](https://s.id/id-jobs-v2)

id-jobs: Because searching for a job shouldn't feel like finding a needle in a haystack... made of more needles.

🇮🇩 **Important:** id-jobs is specifically designed for the Indonesian job market. If you're looking for jobs in Antarctica, you're in the wrong place (but we admire your adventurous spirit!).

## Why id-jobs?

Ever felt like finding a job in Indonesia is like trying to herd cats while juggling flaming torches? Say no more! id-jobs gathers job listings faster than you can say "Aku butuh pekerjaan!"

## How it Works

Picture id-jobs as your personal job-hunting ninja. It stealthily visits Indonesian job websites, grabs the goods, and presents it all in one tidy spreadsheet. No black outfit or throwing stars required!

We currently infiltrate... err, collect data from:
- Jobstreet Indonesia (not to be confused with Sesame Street)
- Glints Indonesia (shinier than regular Indonesia)
- Kalibrr (fun to say, even more fun to find jobs on)
- And more local sources than you can shake a stick at!

## Making Sense of the Data

With all this Indonesian job data at your fingertips, you can:
- Spot trends faster than a teenager spots a new TikTok dance
- Create charts so beautiful, they'll make Excel jealous
- Use spreadsheet functions to analyze the job market (Warning: May cause unexpected bouts of "I love data!")

## Get Involved (for Brave Beginners and Curious Coders)

Ready to dip your toes into the exciting world of web scraping? Don't worry, we won't throw you into the deep end without a floatie! Here's how to get started:

1. **Clone the project:**
   - Think of this as making a copy of our digital treasure map.
   - Visit the [GitHub page](https://github.com/ceroberoz/id-jobs)
   - Click the green "Code" button and copy the URL
   - Open your computer's terminal (Don't panic! It's just a text-based adventure game)
   - Type `git clone [paste URL here]` and press Enter
   - Congratulations! You've just performed your first tech heist (legally, of course)

2. **Set up your Python playground:**
   - Install Python from python.org (It's like LEGO for grown-ups)
   - In the terminal, navigate to the project folder:
     ```
     cd id-jobs
     ```
   - Create a virtual environment (It's like a sandbox, but without the cats):
     ```
     python -m venv venv
     ```
   - Activate your new digital fort:
     - Windows: `venv\Scripts\activate`
     - Mac/Linux: `source venv/bin/activate`
   - You're now in a magical realm where code reigns supreme!

3. **Summon the necessary tools:**
   - Install required packages:
     ```
     pip install -r requirements.txt
     ```
   - Install Playwright (our robotic browser puppet):
     ```
     playwright install
     ```
   - You're now armed with everything you need to conquer the job data world!

4. **Run your first scraper:**
   - To see results appear like magic in your terminal:
     ```
     scrapy crawl jobstreet
     ```
   - To capture your prey (data) in a file:
     ```
     scrapy crawl jobstreet -o jobstreet_jobs.csv -t csv
     ```
   - Watch in awe as job listings materialize before your very eyes!

5. **Experiment and explore:**
   - Try different scrapers by replacing 'jobstreet' with other scraper names
   - Modify the scrapers in the `spiders` folder (Caution: Here be dragons... and exciting possibilities!)
   - Break things, fix things, learn things – it's all part of the coding adventure!

Remember, every master coder started as a beginner. So don't be afraid to make mistakes – they're just plot twists in your coding journey!

Need help? Feel free to open an issue on GitHub. We promise not to laugh... too hard. 😉

Now go forth and scrape responsibly, young data padawan!

## Work in Progress

Some job sources might be playing hard to get. Don't worry, our code cupids are on the case!

## License

id-jobs is open source under the GPL-3.0 license. Use it, tweak it, share it – just keep it open source. It's like a potluck, but for code!

Remember: Always scrape responsibly. No website feelings were harmed in the making of this project!
