# Frequently Asked Questions (FAQ)

## General Questions

1. Q: What is id-jobs?

   A: id-jobs is a tool that collects job listings from various Indonesian job boards and company websites, organizing them into one easy-to-access Google Sheet.

2. Q: Is id-jobs free to use?

   A: Yes, id-jobs is free and open-source under the GPL-3.0 license.

3. Q: How often is the job data updated?

   A: The job data is updated daily through our automated scraping process.

4. Q: Can I use id-jobs for job markets outside of Indonesia?

   A: id-jobs is specifically designed for the Indonesian job market. While you could potentially modify it for other markets, it's not designed for that purpose out of the box.

## Data and Usage

5. Q: How can I access the job data?

   A: You can view the job data in our Google Sheet at [https://s.id/id-jobs-v2](https://s.id/id-jobs-v2).

6. Q: Can I download the data for my own analysis?

   A: Yes, you can download the data from the Google Sheet. Please remember to credit id-jobs if you use the data in any public work.

7. Q: What job boards does id-jobs currently scrape?

   A: We currently scrape data from Jobstreet Indonesia, Glints Indonesia, Kalibrr, TopKarir, Indeed Indonesia, and various company career pages.

8. Q: Is the salary information always available?

   A: Not all job listings include salary information. We collect this data when it's available, but many listings do not provide it.

## Technical Questions

9. Q: What programming language is id-jobs written in?

   A: id-jobs is primarily written in Python, using libraries such as Scrapy and Playwright.

10. Q: Can I contribute to the id-jobs project?

    A: Absolutely! We welcome contributions. Please see our Contributing Guidelines for more information.

11. Q: I'm having trouble setting up the project locally. What should I do?

    A: First, make sure you've followed all steps in our QUICKSTART.md guide. If you're still having issues, please open a GitHub issue with details about the problem you're experiencing.

12. Q: How can I add a new job board to scrape?

    A: To add a new job board, you'll need to create a new spider in the `spiders` directory. Please see our documentation on creating new spiders, or open an issue for guidance.

## Legal and Ethical Questions

13. Q: Is web scraping legal?

    A: Web scraping can be legal, but it depends on how it's done and the website's terms of service. id-jobs is designed to scrape responsibly and in accordance with each site's robots.txt file.

14. Q: Do you store personal information from job listings?

    A: We only collect publicly available information from job listings. We do not collect or store personal information of job seekers or employers.

15. Q: What should I do if I notice incorrect data in the job listings?

    A: Please open a GitHub issue with details about the incorrect data. We'll investigate and correct it as soon as possible.

If you have a question that's not answered here, please feel free to open an issue on our GitHub repository.
