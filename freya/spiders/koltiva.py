import scrapy
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from freya.pipelines import calculate_job_age
from freya.utils import calculate_job_apply_end_date

logger = logging.getLogger(__name__)

class KoltivaSpider(scrapy.Spider):
    name = 'koltiva'
    BASE_URL = 'https://career.koltiva.com'
    API_URL = 'https://erp-api.koltitrace.com/api/v1/jobs?limit=100'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def start_requests(self):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBzYW5qYXlhLndvcmtAZ21haWwuY29tIiwiaWF0IjoxNzI2MTI5NTIwfQ.4NDbf50RCpgcpQ8tz2oPBULtom0o-A5JgJOjDOHXtIY',
            'origin': 'https://career.koltiva.com',
            'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320'
        }
        yield scrapy.Request(self.API_URL, headers=headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        for job in data['data']['data']:
            yield self.parse_job(job)

    def parse_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        first_seen = self.timestamp
        last_seen = self.timestamp

        return {
            'job_title': self.sanitize_string(job_data['position_name'], is_title=True),
            'job_location': f"{self.sanitize_string(job_data['unit_name'])} - {self.sanitize_string(job_data['country_name'])}",
            'job_department': self.sanitize_string(job_data['unitsec_name']),
            'job_url': f"{self.BASE_URL}/job/{job_data['slug']}",
            'first_seen': first_seen,
            'base_salary': 'N/A',
            'job_type': self.sanitize_string(job_data['work_period_name'], is_job_type=True),
            'job_level': self.sanitize_string(job_data['level_name']),
            'job_apply_end_date': job_data['close_date'].split('T')[0],
            'last_seen': last_seen,
            'is_active': 'True',
            'company': 'Koltiva',
            'company_url': self.BASE_URL,
            'job_board': 'Koltiva Careers',
            'job_board_url': self.BASE_URL,
            'job_age': calculate_job_age(first_seen, last_seen),
            'work_arrangement': self.get_work_arrangement(job_data['jobs_benefits_perks']),
        }

    def get_work_arrangement(self, benefits: str) -> str:
        return 'Remote' if 'Work-from-home' in benefits else 'On-site'

    @staticmethod
    def sanitize_string(s: Optional[str], is_title: bool = False, is_job_type: bool = False) -> str:
        if s is None:
            return 'N/A'
        s = s.strip()
        s = s.replace(',', ' -')  # Replace commas with hyphens for CSV compatibility
        if is_title:
            s = s.title()
        elif is_job_type:
            s = s.replace('Contract', '').strip()
        return ' '.join(s.split()) or 'N/A'
