import scrapy
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class KalibrrSpiderJson(scrapy.Spider):
    name = 'kalibrr'
    BASE_URL = 'https://www.kalibrr.com/kjs/job_board/search?limit=2000&offset={}'
    JOB_URL_TEMPLATE = "https://www.kalibrr.com/c/{}/jobs/{}"
    COMPANY_URL_TEMPLATE = "https://www.kalibrr.com/id-ID/c/{}/jobs"
    JOB_BOARD_URL = 'https://www.kalibrr.com/id-ID/home'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def start_requests(self):
        yield scrapy.Request(
            self.BASE_URL.format(0),
            headers={'Content-Type': 'application/json'},
            callback=self.parse
        )

    def parse(self, response):
        try:
            data = json.loads(response.text)
            jobs = data.get('jobs', [])

            for job in jobs:
                yield self.parse_job(job)

            self.handle_pagination(data)

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def handle_pagination(self, data: Dict[str, Any]):
        total_jobs = data.get('total', 0)
        current_offset = data.get('offset', 0)
        jobs = data.get('jobs', [])
        if current_offset + len(jobs) < total_jobs:
            next_offset = current_offset + len(jobs)
            yield scrapy.Request(
                self.BASE_URL.format(next_offset),
                callback=self.parse
            )

    def parse_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'job_title': self.sanitize_string(job.get('name')),
            'job_location': self.get_job_location(job),
            'job_department': 'N/A',
            'job_url': self.get_job_url(job),
            'first_seen': self.timestamp,
            'base_salary': job.get('base_salary'),
            'job_type': job.get('tenure'),
            'job_level': 'N/A',
            'job_apply_end_date': job.get('application_end_date'),
            'last_seen': '',
            'is_active': 'True',
            'company': job.get('company_name'),
            'company_url': self.get_company_url(job),
            'job_board': 'Kalibrr',
            'job_board_url': self.JOB_BOARD_URL
        }

    @staticmethod
    def sanitize_string(s: Optional[str]) -> str:
        return s.replace(", ", " - ") if s else 'N/A'

    @staticmethod
    def get_job_location(job: Dict[str, Any]) -> str:
        return job.get('google_location', {}).get('address_components', {}).get('city', 'N/A')

    def get_job_url(self, job: Dict[str, Any]) -> str:
        company_code = job.get('company_info', {}).get('code', '')
        job_id = job.get('id', '')
        return self.JOB_URL_TEMPLATE.format(company_code, job_id)

    def get_company_url(self, job: Dict[str, Any]) -> str:
        company_code = job.get('company_info', {}).get('code', '')
        return self.COMPANY_URL_TEMPLATE.format(company_code)