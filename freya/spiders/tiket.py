import scrapy
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional, List
import random
from freya.pipelines import calculate_job_age  # Import the function
from freya.utils import calculate_job_apply_end_date

logger = logging.getLogger(__name__)

class TiketSpiderJson(scrapy.Spider):
    name = 'tiket'
    BASE_URL = 'https://api.lever.co/v0/postings/tiket?mode=json'

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
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Origin': 'https://careers.tiket.com',
            'Pragma': 'no-cache',
            'Referer': 'https://careers.tiket.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': random.choice(self.USER_AGENTS),
            'dnt': '1',
            'sec-gpc': '1'
        }
        yield scrapy.Request(self.BASE_URL, headers=headers, callback=self.parse)

    def parse(self, response):
        try:
            data = json.loads(response.text)
            for job in data:
                yield self.parse_job(job)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            logger.debug(f"Response content: {response.text}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def parse_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        first_seen = datetime.strptime(self.timestamp, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        last_seen = self.format_unix_time(job.get('createdAt'))
        
        return {
            'job_title': self.sanitize_string(job.get('text')),
            'job_location': self.sanitize_string(job.get('categories', {}).get('location')),
            'job_department': self.sanitize_string(job.get('categories', {}).get('department')),
            'job_url': job.get('hostedUrl'),
            'first_seen': first_seen,
            'base_salary': 'N/A',
            'job_type': self.sanitize_string(job.get('categories', {}).get('commitment')),
            'job_level': 'N/A',
            'job_apply_end_date': calculate_job_apply_end_date(last_seen),
            'last_seen': last_seen,
            'is_active': 'True',
            'company': 'Tiket.com',
            'company_url': 'https://careers.tiket.com',
            'job_board': 'Tiket.com Careers',
            'job_board_url': 'https://careers.tiket.com',
            'job_age': calculate_job_age(first_seen, last_seen),
            'work_arrangement': self.extract_work_arrangement(job),

            # Optional fields
            # 'job_description': self.sanitize_string(job.get('descriptionPlain')),
            # 'job_qualifications': self.extract_qualifications(job.get('lists', [])),
            # 'job_responsibilities': self.extract_responsibilities(job.get('lists', [])),
            # 'job_team': self.sanitize_string(job.get('categories', {}).get('team')),
            # 'job_country': job.get('country', 'N/A'),
            # 'apply_url': job.get('applyUrl'),
        }

    @staticmethod
    def sanitize_string(s: Optional[str]) -> str:
        if s is None:
            return 'N/A'
        return s.replace(',', ' -').strip()

    @staticmethod
    def format_unix_time(unix_time: Optional[int]) -> str:
        if unix_time is None:
            return 'N/A'
        try:
            return datetime.fromtimestamp(unix_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            return 'N/A'

    def extract_qualifications(self, lists: List[Dict[str, Any]]) -> str:
        for item in lists:
            if "Mandatory belongings" in item.get('text', ''):
                return self.sanitize_string(item.get('content', ''))
        return 'N/A'

    def extract_responsibilities(self, lists: List[Dict[str, Any]]) -> str:
        for item in lists:
            if "Your main duties" in item.get('text', ''):
                return self.sanitize_string(item.get('content', ''))
        return 'N/A'

    def extract_work_arrangement(self, job: Dict[str, Any]) -> str:
        # Implement logic to extract work arrangement from job data
        # This is just an example, adjust according to the actual data structure
        return job.get('workplaceType', 'N/A')