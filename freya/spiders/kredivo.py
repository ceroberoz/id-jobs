import scrapy
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from freya.pipelines import calculate_job_age
from freya.utils import calculate_job_apply_end_date

logger = logging.getLogger(__name__)

class FlipSpider(scrapy.Spider):
    name = 'flip'
    BASE_URL = 'https://career.flip.id'
    CAREERS_URL = f"{BASE_URL}/jobs"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def start_requests(self):
        yield scrapy.Request(self.CAREERS_URL, meta={"playwright": True}, callback=self.parse)

    def parse(self, response):
        for job_card in response.css('div.job-list a.heading'):
            yield self.parse_job(job_card)

    def parse_job(self, selector) -> Dict[str, Any]:
        first_seen = self.timestamp
        last_seen = self.timestamp

        job_title = self.sanitize_string(selector.css('div.job-title::text').get())
        job_location = self.sanitize_string(selector.css('div.location-info::text').get().split('\n')[0])
        job_type = self.sanitize_string(selector.css('div.location-info::text').get().split('\n')[-1])
        # job_description = self.sanitize_string(selector.css('div.job-desc::text').get())
        job_url = self.BASE_URL + selector.css('::attr(href)').get()

        return {
            'job_title': job_title,
            'job_location': job_location,
            'job_department': self.get_department(selector),
            'job_url': job_url,
            'first_seen': first_seen,
            'base_salary': 'N/A',
            'job_type': job_type,
            'job_level': 'N/A',
            'job_apply_end_date': calculate_job_apply_end_date(last_seen),
            'last_seen': last_seen,
            'is_active': 'True',
            'company': 'Flip',
            'company_url': self.BASE_URL,
            'job_board': 'Flip',
            'job_board_url': self.CAREERS_URL,
            'job_age': calculate_job_age(first_seen, last_seen),
            'work_arrangement': self.get_work_arrangement(job_location),
            # 'job_description': job_description,
        }

    def get_department(self, selector) -> str:
        department = selector.xpath('ancestor::li/@data-portal-role').get()
        return department.replace('_role_', '') if department else 'N/A'

    def get_work_arrangement(self, location: str) -> str:
        return 'Remote' if 'Remote' in location else 'On-site'

    @staticmethod
    def sanitize_string(s: Optional[str]) -> str:
        return ' '.join(s.strip().split()) if s else 'N/A'