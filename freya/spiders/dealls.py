import scrapy
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class DeallsSpiderJson(scrapy.Spider):
    name = 'dealls'
    BASE_URL = 'https://api.sejutacita.id/v1/explore-job/job'
    JOBS_PER_PAGE = 18

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def start_requests(self):
        headers = {'Content-Type': 'application/json'}
        url = self.get_paginated_url(1)
        yield scrapy.Request(url, headers=headers, callback=self.parse)

    def get_paginated_url(self, page: int) -> str:
        return f"{self.BASE_URL}?page={page}&limit={self.JOBS_PER_PAGE}&published=true&status=active&prioritizeNonFilledApplicantQuota=true&sortBy=asc&sortParam=mostRelevant&includeNegotiableSalary=true&salaryMax=0"

    def parse(self, response):
        try:
            data = json.loads(response.text)
            jobs = data['data']['docs']
            for job in jobs:
                yield self.parse_job(job)

            current_page = data['data']['page']
            max_pages = data['data']['totalPages']
            if current_page < max_pages:
                next_page = current_page + 1
                next_page_url = self.get_paginated_url(next_page)
                yield scrapy.Request(next_page_url, callback=self.parse)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            logger.debug(f"Response content: {response.text}")

    def parse_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'job_title': self.sanitize_string(job['role']),
            'job_location': self.get_job_location(job),
            'job_department': self.get_job_department(job),
            'job_url': f"https://dealls.com/role/{job['slug']}",
            'first_seen': self.timestamp,
            'base_salary': self.get_job_salary(job),
            'job_type': job['employmentTypes'],
            'job_level': 'N/A',
            'job_apply_end_date': '',
            'last_seen': self.format_datetime(job['latestUpdatedAt']),
            'is_active': 'True',
            'company': job['company']['name'],
            'company_url': 'N/A',
            'job_board': 'Dealls',
            'job_board_url': 'https://dealls.com/'
        }

    @staticmethod
    def sanitize_string(s: Optional[str]) -> str:
        return s.replace(", ", " - ") if s else 'N/A'

    @staticmethod
    def get_job_department(job: Dict[str, Any]) -> str:
        department = job.get('categorySlug')
        return department.replace("-", " ").title() if department else 'N/A'

    @staticmethod
    def get_job_salary(job: Dict[str, Any]) -> str:
        salary_range = job.get('salaryRange')
        return str(salary_range['start']) if salary_range else 'N/A'

    @staticmethod
    def get_job_location(job: Dict[str, Any]) -> str:
        city = job.get('city', {})
        return city.get('name', 'Remote') if city else 'Remote'

    @staticmethod
    def format_datetime(date_string: str) -> str:
        try:
            dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return date_string  # Return original string if parsing fails