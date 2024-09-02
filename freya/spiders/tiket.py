import scrapy
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional
import random

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
        return {
            'job_title': self.sanitize_string(job.get('text')),
            'job_location': self.sanitize_string(job.get('categories', {}).get('location')),
            'job_department': self.sanitize_string(job.get('categories', {}).get('department')),
            'job_url': job.get('hostedUrl'),
            'first_seen': self.timestamp,
            'base_salary': 'N/A',
            'job_type': self.sanitize_string(job.get('categories', {}).get('commitment')),
            'job_level': 'N/A',
            'job_apply_end_date': 'N/A',
            'last_seen': self.format_unix_time(job.get('createdAt')),
            'is_active': 'True',
            'company': 'Tiket.com',
            'company_url': 'https://careers.tiket.com',
            'job_board': 'Tiket.com Careers',
            'job_board_url': 'https://careers.tiket.com'
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