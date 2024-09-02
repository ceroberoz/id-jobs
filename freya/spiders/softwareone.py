import scrapy
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional
import random
from freya.pipelines import calculate_job_age  # Import the function


logger = logging.getLogger(__name__)

class SoftwareOneSpiderJson(scrapy.Spider):
    name = 'softwareone'
    BASE_URL = 'https://careers.softwareone.com'
    API_URL = f'{BASE_URL}/api/jobs?country=Indonesia&page=1&sortBy=posted_date&descending=true&internal=false&deviceId=undefined&domain=softwareone.jibeapply.com'

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
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'dnt': '1',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://careers.softwareone.com/en/jobs?country=Indonesia&page=1',
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
            jobs = data.get('jobs', [])

            if not jobs:
                logger.info("No jobs found for the given criteria.")
                return

            for job in jobs:
                yield self.parse_job(job['data'])

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            logger.debug(f"Response content: {response.text}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def parse_job(self, job):
        first_seen = datetime.strptime(self.timestamp, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        last_seen = self.format_posted_date(job.get('posted_date', 'N/A'))
        
        return {
            'job_title': job.get('title', 'N/A'),
            'job_location': job.get('full_location', 'N/A'),
            'job_department': job.get('tags2', ['N/A'])[0] if job.get('tags2') else 'N/A',
            'job_url': f"https://careers.softwareone.com/en/jobs/{job.get('req_id', '')}",
            'first_seen': first_seen,
            'base_salary': 'N/A',  # Salary information is not provided in the API response
            'job_type': job.get('employment_type', 'N/A'),
            'job_level': 'N/A',  # Job level is not directly provided in the API response
            'job_apply_end_date': 'N/A',  # Application end date is not provided in the API response
            'last_seen': last_seen,
            'is_active': 'True',
            'company': job.get('hiring_organization', 'SoftwareOne'),
            'company_url': 'https://careers.softwareone.com',
            'job_board': 'SoftwareOne Careers',
            'job_board_url': 'https://careers.softwareone.com/en/jobs',
            'job_age': calculate_job_age(first_seen, last_seen)  # Ensure this line is present

            # Optional fields
            # 'job_description': job.get('description', 'N/A'),
            # 'job_qualifications': job.get('qualifications', 'N/A'),
            # 'job_responsibilities': job.get('responsibilities', 'N/A'),
            # 'job_posted_date': self.format_posted_date(job.get('posted_date', 'N/A')),
            # 'job_id': job.get('req_id', 'N/A'),
            # 'job_categories': ', '.join(job.get('tags2', [])) if job.get('tags2') else 'N/A',
            # 'job_street_address': job.get('street_address', 'N/A'),
            # 'job_city': job.get('city', 'N/A'),
            # 'job_country': job.get('country', 'N/A'),
            # 'job_postal_code': job.get('postal_code', 'N/A')
        }

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

    def format_posted_date(self, date_string):
        try:
            # Parse the date string
            date_obj = datetime.strptime(date_string, "%B %d, %Y")
            # Format the date as YYYY-MM-DD HH:MM:SS
            return date_obj.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            # If parsing fails, return the original string
            return date_string