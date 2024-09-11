import scrapy
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from freya.pipelines import calculate_job_age
from freya.utils import calculate_job_apply_end_date

logger = logging.getLogger(__name__)

class KredivoSpider(scrapy.Spider):
    name = 'kredivo'
    BASE_URL = 'https://careers.kredivocorp.com'
    CAREERS_URL = f"{BASE_URL}/jobs"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def start_requests(self):
        yield scrapy.Request(self.CAREERS_URL, meta={"playwright": True}, callback=self.parse)

    def parse(self, response):
        for job_card in response.css('ul.positions.location li.position'):
            yield self.parse_job(job_card)

    def parse_job(self, selector) -> Dict[str, Any]:
        first_seen = self.timestamp
        last_seen = self.timestamp

        job_title = self.sanitize_string(selector.css('h2::text').get(), is_title=True)
        job_location = self.sanitize_string(selector.css('li.location span::text').get())
        job_type = self.sanitize_string(selector.css('li.type span::text').get(), is_job_type=True)
        job_department = self.sanitize_string(selector.css('li.department span::text').get())
        job_url = self.BASE_URL + selector.css('a::attr(href)').get()

        return {
            'job_title': job_title,
            'job_location': job_location,
            'job_department': job_department,
            'job_url': job_url,
            'first_seen': first_seen,
            'base_salary': 'N/A',
            'job_type': job_type,
            'job_level': self.extract_job_level(job_title),
            'job_apply_end_date': calculate_job_apply_end_date(last_seen),
            'last_seen': last_seen,
            'is_active': 'True',
            'company': 'Kredivo',
            'company_url': self.BASE_URL,
            'job_board': 'Kredivo Careers',
            'job_board_url': self.CAREERS_URL,
            'job_age': calculate_job_age(first_seen, last_seen),
            'work_arrangement': self.get_work_arrangement(job_location),
        }

    def extract_job_level(self, job_title: str) -> str:
        levels = ['Intern', 'Junior', 'Senior', 'Lead', 'Manager', 'Head', 'Director', 'VP', 'C-level']
        for level in levels:
            if level.lower() in job_title.lower():
                return level
        return 'N/A'

    def get_work_arrangement(self, location: str) -> str:
        return 'Remote' if 'Remote' in location else 'On-site'

    @staticmethod
    def sanitize_string(s: Optional[str], is_title: bool = False, is_job_type: bool = False) -> str:
        if s is None:
            return 'N/A'
        s = s.strip()
        if is_title:
            s = s.replace(',', ' -')
        elif is_job_type:
            s = s.replace('%', '').strip()
            if 'LABEL_POSITION_TYPE' in s:
                s = s.split('LABEL_POSITION_TYPE_')[-1].strip()
        return ' '.join(s.split()) or 'N/A'