import scrapy
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from freya.pipelines import calculate_job_age
from freya.utils import calculate_job_apply_end_date

logger = logging.getLogger(__name__)

class MekariSpider(scrapy.Spider):
    name = 'mekari'
    BASE_URL = 'https://mekari.hire.trakstar.com'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def start_requests(self):
        yield scrapy.Request(
            self.BASE_URL,
            headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320'
            },
            callback=self.parse
        )

    def parse(self, response):
        try:
            for job in response.css('div.js-card.list-item'):
                yield self.parse_job(job)

            self.handle_pagination(response)
        except Exception as e:
            logger.error(f"Error parsing page: {e}")

    def parse_job(self, selector) -> Dict[str, Any]:
        first_seen = self.timestamp
        last_seen = self.timestamp

        job_title = self.sanitize_string(selector.css('h3.js-job-list-opening-name::text').get())
        job_location = self.sanitize_string(selector.css('div.js-job-list-opening-loc::text').get())
        job_department = self.sanitize_string(selector.css('div.col-md-4.col-xs-12 div.rb-text-4:first-child::text').get())
        job_type = self.sanitize_string(selector.css('div.js-job-list-opening-meta span:first-child::text').get())
        work_arrangement = self.sanitize_string(selector.css('div.js-job-list-opening-meta span:last-child::text').get())

        job_url = self.BASE_URL + selector.css('a::attr(href)').get()

        return {
            'job_title': job_title,
            'job_location': job_location,
            'job_department': job_department,
            'job_url': job_url,
            'first_seen': first_seen,
            'base_salary': 'N/A',
            'job_type': job_type,
            'job_level': 'N/A',
            'job_apply_end_date': calculate_job_apply_end_date(last_seen),
            'last_seen': last_seen,
            'is_active': 'True',
            'company': 'Mekari',
            'company_url': self.BASE_URL,
            'job_board': 'Mekari',
            'job_board_url': self.BASE_URL,
            'job_age': calculate_job_age(first_seen, last_seen),
            'work_arrangement': work_arrangement,
        }

    @staticmethod
    def sanitize_string(s: Optional[str]) -> str:
        if s:
            return ' - '.join(part.strip() for part in s.split(',') if part.strip())
        return 'N/A'

    def handle_pagination(self, response):
        next_page = response.css('ul.pagination li.page-item:last-child a::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
