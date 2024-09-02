import scrapy
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional
import random

logger = logging.getLogger(__name__)

class BlibliSpiderJson(scrapy.Spider):
    name = 'blibli'
    BASE_URL = 'https://careers.blibli.com'
    API_URL = f'{BASE_URL}/ext/api/job/list?format=COMPLETE&groupBy=true'
    JOB_URL_TEMPLATE = f'{BASE_URL}/job-detail/{{}}?job={{}}'

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def start_requests(self):
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'dnt': '1',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://careers.blibli.com/department/all-departments?experience=&employmentType=',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': random.choice(self.USER_AGENTS)
        }
        yield scrapy.Request(self.API_URL, headers=headers, callback=self.parse)

    def parse(self, response):
        try:
            data = json.loads(response.text)
            departments = data['responseObject']

            for department in departments:
                for job in department['jobs']:
                    yield self.parse_job(job)

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            logger.debug(f"Response content: {response.text}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def parse_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'job_title': self.sanitize_string(job.get('title')),
            'job_location': self.sanitize_string(job.get('location')),
            'job_department': self.sanitize_string(job.get('departmentName')),
            'job_url': self.get_job_url(job),
            'first_seen': self.timestamp,
            'base_salary': 'N/A',
            'job_type': self.get_employment_type(job),
            'job_level': self.sanitize_string(job.get('experience')),
            'job_apply_end_date': 'N/A',
            'last_seen': self.format_unix_time(job.get('createdDate')),
            'is_active': 'True',
            'company': 'Blibli',
            'company_url': self.BASE_URL,
            'job_board': 'Blibli Job Portal',
            'job_board_url': 'https://careers.blibli.com'
        }

    def get_job_url(self, job: Dict[str, Any]) -> str:
        job_title = job.get('title', '').lower().replace(' ', '-')
        job_id = job.get('id', '')
        return self.JOB_URL_TEMPLATE.format(job_title, job_id)

    @staticmethod
    def get_employment_type(job: Dict[str, Any]) -> str:
        employment_type = job.get('employmentType', '')
        return employment_type.replace("Ph-", "").replace("-", " ").capitalize() if employment_type else 'N/A'

    @staticmethod
    def sanitize_string(s: Optional[str]) -> str:
        return s.strip() if s else 'N/A'

    @staticmethod
    def format_unix_time(unix_time: Optional[int]) -> str:
        if unix_time is None:
            return 'N/A'
        try:
            return datetime.fromtimestamp(unix_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            return 'N/A'