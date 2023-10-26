# id-jobs
Indonesia job information, hand picked from trusted sources.

Explore the coolest **Bare Lazy Minimum Product** in Google Sheets format! 

https://s.id/id-jobs

Made with Python and Scrapy with Codeium.
[![built with Codeium](https://codeium.com/badges/main)](https://codeium.com)

=========================================================================

# Job source list:
- **company**
	- [X] Vidio
	- [ ] Gojek
	- [ ] Tokopedia
	- [ ] Blibli
	- [X] Evermos
	- [X] SehatQ

- **job-portal**
	- [X] Kalibrr
	- [ ] JobsDB
	- [ ] Glints
	- [X] Dealls
	- [ ] Jobstreet

# data-enrichment
- **Event**
	- [ ] Dicoding
	- [ ] Binar Academy
- **About company**
	- [ ] LinkedIn
	- [ ] Crunchbase
- **News / rumor mills**
	-  [ ] Dailymotion
	-  [ ] e27
	-  [ ] DealStreetAsia
	-  [ ] TechInAsia

# How to run
1. Clone this repository
2. Create venv ```python3 -m venv venv```
3. Run the script
-Run the script ```pip install -r requirements.txt```
-Run the script ```playwright install```
4. Run ```scrapy crawl crawler-name```

More information about Scrapy: https://docs.scrapy.org/en/latest/intro/overview.html
More information about Scrapy Playwright: https://playwright.dev/docs/intro