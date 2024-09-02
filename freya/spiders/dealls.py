import scrapy
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional
import random
from freya.pipelines import calculate_job_age  # Import the function


logger = logging.getLogger(__name__)

class DeallsSpiderJson(scrapy.Spider):
    name = 'dealls'
    BASE_URL = 'https://api.sejutacita.id/v1/explore-job/job'
    JOBS_PER_PAGE = 18
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'
    ]

    @classmethod
    def get_random_user_agent(cls):
        return random.choice(cls.USER_AGENTS)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def start_requests(self):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'dnt': '1',
            'origin': 'https://dealls.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://dealls.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'sec-gpc': '1',
            'user-agent': self.get_random_user_agent()
        }
        url = self.get_paginated_url(1)
        yield scrapy.Request(url, headers=headers, callback=self.parse)

    def get_paginated_url(self, page: int) -> str:
        return f"{self.BASE_URL}?page={page}&sortParam=mostRelevant&sortBy=asc&published=true&limit={self.JOBS_PER_PAGE}&status=active"

    def parse(self, response):
        try:
            data = json.loads(response.text)
            jobs = data['data']['docs']
            for job in jobs:
                yield self.parse_job(job)

            current_page = data['data']['page']
            total_pages = data['data']['totalPages']
            if current_page < total_pages:
                next_page = current_page + 1
                next_page_url = self.get_paginated_url(next_page)
                yield scrapy.Request(next_page_url, callback=self.parse)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            logger.debug(f"Response content: {response.text}")

    def parse_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        first_seen = datetime.strptime(self.timestamp, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        last_seen = self.format_datetime(job.get('latestUpdatedAt', ''))
        
        return {
            'job_title': self.sanitize_string(job.get('role', '')),
            'job_location': self.get_job_location(job),
            'job_department': self.get_job_department(job),
            'job_url': f"https://dealls.com/role/{job.get('slug', '')}",
            'first_seen': first_seen,
            'base_salary': self.get_job_salary(job),
            'job_type': ', '.join(job.get('employmentTypes', [])),
            'job_level': self.get_job_level(job),
            'job_apply_end_date': '',
            'last_seen': last_seen,
            'is_active': str(job.get('status', '') == 'active'),
            'company': job.get('company', {}).get('name', ''),
            'company_url': f"https://dealls.com/company/{job.get('company', {}).get('slug', '')}",
            'job_board': 'Dealls',
            'job_board_url': 'https://dealls.com/',
            'job_age': calculate_job_age(first_seen, last_seen)  # Ensure this line is present

            # Optional fields
            # 'workplace_type': job['workplaceType'],
            # 'skills': ', '.join([skill['name'] for skill in job['skills']]),
            # 'company_sector': job['company']['sector'],
            # 'company_funding_stage': job['company']['insight']['fundingStage'],
            # 'company_funding_amount': job['company']['insight']['fundingAmount'],
            # 'urgently_needed': str(job['urgentlyNeeded']),
            # 'published_at': self.format_datetime(job['publishedAt']),
            # 'country': job['country']['name']
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

    def get_job_location(self, job: Dict[str, Any]) -> str:
        city = job.get('city', {})
        country = job.get('country', {})
        city_name = city.get('name', 'N/A') if city else 'N/A'
        country_name = country.get('name', 'N/A') if country else 'N/A'
        return f"{city_name}, {country_name}"

    def get_job_level(self, job: Dict[str, Any]) -> str:
        educations = job['candidatePreference']['lastEducations']
        if 7 in educations:
            return "Postgraduate"
        elif 6 in educations:
            return "Graduate"
        elif 5 in educations:
            return "Undergraduate"
        else:
            return "N/A"

    @staticmethod
    def format_datetime(date_string: str) -> str:
        try:
            dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return date_string  # Return original string if parsing fails